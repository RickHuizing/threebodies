#ifndef THREEBODY2D_HPP
#define THREEBODY2D_HPP

#include "energy.hpp"
#include <NumCpp.hpp>

// TODO: remove
#include <iostream>

template <typename T>
void compute_a(const nc::NdArray<T> &x, const nc::NdArray<T> &y, const nc::NdArray<T> &M, nc::NdArray<T> &ax, nc::NdArray<T> &ay, const T &G, nc::NdArray<T> &axOut, nc::NdArray<T> &ayOut)
{
    for (int j = 0; j < 3; j++)
    {

        // Compute the distance between current body and the others(also with itself)
        nc::NdArray<T> dx = ((nc::NdArray<T>)(x[j] - x)); // TODO: check if conjugate and transpose can be left out
        nc::NdArray<T> dy = ((nc::NdArray<T>)(y[j] - y)); //.transpose();

        // Compute the acceleration according to Newton law

        ax.put(ax.rSlice(), j, ((nc::multiply(-dx, M) * G) / (nc::power((nc::NdArray<T>)nc::sqrt(nc::power(dx, 2) + nc::power(dy, 2)), 3))).transpose());
        ay.put(ay.rSlice(), j, ((nc::multiply(-dy, M) * G) / (nc::power((nc::NdArray<T>)nc::sqrt(nc::power(dx, 2) + nc::power(dy, 2)), 3))).transpose());

        ax = nc::nan_to_num(ax); // Replace NaN with 0's
        ay = nc::nan_to_num(ay);
    }
    axOut = nc::sum(ax, nc::Axis::ROW);
    ayOut = nc::sum(ay, nc::Axis::ROW);
}

template <typename T>
int compute_verlet(T step_size, nc::NdArray<T> &x, nc::NdArray<T> &y, nc::NdArray<T> &M, nc::NdArray<T> &ax, nc::NdArray<T> &ay, T &G, nc::NdArray<T> &vx, nc::NdArray<T> &vy)
{
    // Compute total energy of the system at start. This should stay constant
    const T startEnergy = totalEnergy<T>(G, M, x(0, x.cSlice()), y(0, y.cSlice()), vx(0, vx.cSlice()), vy(0, vy.cSlice()));
    const T maxErr = 0.05;

    const T half_step_size_sq = 0.5 * (step_size * step_size);
    const T half_step_size = 0.5 * step_size;
    for (int i = 0; i < x.shape().rows - 1; i++)
    {
        // Compute current acceleration
        nc::NdArray<T> ax_tot, ay_tot;
        compute_a<T>(x(i, x.cSlice()), y(i, y.cSlice()), M, ax, ay, G, ax_tot, ay_tot);

        // Update the position
        nc::NdArray<T> nx = x(i, x.cSlice()) + step_size * vx(i, vx.cSlice()) + half_step_size_sq * ax_tot;
        nc::NdArray<T> ny = y(i, y.cSlice()) + step_size * vy(i, vy.cSlice()) + half_step_size_sq * ay_tot;

        const T energyErr = totalEnergy<T>(G, M, x, y, vx, vy) / startEnergy;

        if (energyErr < 1 - maxErr || energyErr > 1 + maxErr)
        {
            std::cout << "Kinetic energy: " << kineticEnergy<T>(G, M, x(i, x.cSlice()), y(i, y.cSlice()), vx(i, vx.cSlice()), vy(i, vy.cSlice())) << std::endl;
            std::cout << "potential energy: " << potentialEnergy<T>(G, M, x(i, x.cSlice()), y(i, y.cSlice()), vx(i, vx.cSlice()), vy(i, vy.cSlice())) << std::endl;

            std::cout << "total Energy: " << totalEnergy<T>(G, M, x(i, x.cSlice()), y(i, y.cSlice()), vx(i, vx.cSlice()), vy(i, vy.cSlice())) << std::endl;
            return i + 1;
        }

        // early stop - bodies too far apart
        if (nc::max(nx)[0] > 3 || nc::max(ny)[0] > 3 || nc::min(nx)[0] < -3 || nc::min(ny)[0] < -3)
        {
            return i + 1;
        }

        x.put(i + 1, x.cSlice(), nx);
        y.put(i + 1, y.cSlice(), ny);

        // Compute the next time acceleration
        nc::NdArray<T> ax_tot_next, ay_tot_next;
        compute_a<T>(x(i+1, x.cSlice()), y(i+1, y.cSlice()), M, ax, ay, G, ax_tot_next, ay_tot_next);

        // Compute the next time velocity according to the Verlet method
        vx.put(i + 1, vx.cSlice(), vx(i, vx.cSlice()) + half_step_size * (ax_tot + ax_tot_next));
        vy.put(i + 1, vy.cSlice(), vy(i, vy.cSlice()) + half_step_size * (ay_tot + ay_tot_next));
    }
    return -1; // success
}

// WARNING: not tested, not sure if correct
template <typename T>
int compute_euler(T step_size, nc::NdArray<T> &x, nc::NdArray<T> &y, nc::NdArray<T> &M, nc::NdArray<T> &ax, nc::NdArray<T> &ay, T &G, nc::NdArray<T> &vx, nc::NdArray<T> &vy) 
{
    // simple euler method
    for (int i = 0; i < x.shape().rows; i++)
    {
        // Compute current acceleration
        nc::NdArray<T> ax_tot, ay_tot;
        nc::NdArray<T> xSlice = x(i, x.cSlice());
        nc::NdArray<T> ySlice = y(i, y.cSlice());
        compute_a<T>(xSlice, ySlice, M, ax, ay, G, ax_tot, ay_tot);

        // Update the position
        x.put(i + 1, x.cSlice(), step_size * vx(i, vx.cSlice()));
        y.put(i + 1, y.cSlice(), step_size * vy(i, vy.cSlice()));

        // update the velocity
        vx.put(i + 1, vx.cSlice(), vx(i, vx.cSlice()) + step_size * ax_tot);
        vy.put(i + 1, vy.cSlice(), vy(i, vy.cSlice()) + step_size * ay_tot);

        // failure - bodies too far apart
        if (nc::max(x(i+1, x.cSlice()))[0] > 3 || nc::max(y(i+1, y.cSlice()))[0] > 3 || nc::min(x(i+1, x.cSlice()))[0] < -3 || nc::min(y(i+1, y.cSlice()))[0] < -3)
        {
            return i + 1;
        }
    }
    // success
    return -1;
}
#endif