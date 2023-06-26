#ifndef ENERGY_HPP
#define ENERGY_HPP

#include <NumCpp.hpp>

template <typename T>
T potentialEnergy(const T G, const nc::NdArray<T> &M, const nc::NdArray<T> &x, const nc::NdArray<T> &y, const nc::NdArray<T> &vx, const nc::NdArray<T> &vy)
{
    T sum = 0;

    for (int i = 0; i < 3; i++)
    {
        for (int j = 0; j < 3; j++)
        {
            if (i == j)
            {
                continue;
            }
            const T dist = sqrt(pow(x(0, i) - x(0, j), 2) + pow(y(0, i) - y(0, j), 2));

            sum += M(0, i) * M(0, j) / dist;
        }
    }

    return -G * sum;
}

template <typename T>
T kineticEnergy(const T G, const nc::NdArray<T> &M, const nc::NdArray<T> &x, const nc::NdArray<T> &y, const nc::NdArray<T> &vx, const nc::NdArray<T> &vy)
{
    T sum = 0;
    for (int i = 0; i < 3; i++)
    {
        const T velocity = sqrt(pow(vx(0, i), 2) + pow(vy(0, i), 2));
        sum += 1.0 / 2.0 * M(0, i) * velocity;
    }
    return sum;
}

template <typename T>
T totalEnergy(const T G, const nc::NdArray<T> &M, const nc::NdArray<T> &x, const nc::NdArray<T> &y, const nc::NdArray<T> &vx, const nc::NdArray<T> &vy)
{
    return potentialEnergy<T>(G, M, x, y, vx, vy) + kineticEnergy<T>(G, M, x, y, vx, vy);
}

#endif