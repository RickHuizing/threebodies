#include "threebody2d.hpp"
#include "config.hpp"
#include <NumCpp.hpp>
#include <chrono>
#include <filesystem>
#include <quadmath.h>
#include <numeric>
#include <omp.h>

using namespace std;
using namespace nc;

template <typename T>
void init_next_random_iteration(NdArray<T> &x, NdArray<T> &y, NdArray<T> &vx, NdArray<T> &vy, NdArray<T> &ax, NdArray<T> &ay)
{
    // procedure followed by breen et al. (figure 1)
    const T x1 = 1;
    const T y1 = 0;

    const T x2 = -0.5 + 0.5 * nc::random::randN<T>();
    const T y2_max = cos(x2);
    const T y2 = 0 + y2_max * nc::random::randN<T>();

    const T x3 = -x1 - x2;
    const T y3 = -y2;

    x.put(0, 0, x1);
    x.put(0, 1, x2);
    x.put(0, 2, x3);

    y.put(0, 0, y1);
    y.put(0, 1, y2);
    y.put(0, 2, y3);

    vx.put(0, vx.cSlice(), 0);
    vy.put(0, vy.cSlice(), 0);

    ax.put(0, ax.cSlice(), 0);
    ay.put(0, ay.cSlice(), 0);
}
template <typename T>
void save_data(const string &result_id, Config<T> config, NdArray<T> &x, NdArray<T> &y, NdArray<T> &vx, NdArray<T> &vy)
{
    string folder;
    folder.append(config.get_path());
    folder.append(result_id);
    folder.append("/");

    string filename;
    filename.append(folder);
    filename.append("x.dat");

    filesystem::create_directory(folder);

    nc::tofile(x, filename);

    filename = folder;
    filename.append("y.dat");
    nc::tofile(y, filename);

    filename = folder;
    filename.append("vx.dat");
    nc::tofile(vx, filename);

    filename = folder;
    filename.append("vy.dat");
    nc::tofile(vy, filename);
}

template <typename T>
void generateData(Config<T> config, size_t start = 0, size_t end = 0)
{
    // Create output directory
    filesystem::create_directory(config.get_path());

    // initialize x, y, velocity and acceleration vectors
    size_t time_steps = config.time_vector().shape().cols;

    NdArray<T> x = nc::zeros<T>(time_steps, 3);
    NdArray<T> y = nc::zeros<T>(time_steps, 3);
    NdArray<T> vx = nc::zeros<T>(time_steps, 3);
    NdArray<T> vy = nc::zeros<T>(time_steps, 3);
    NdArray<T> ax = nc::zeros<T>(3, 3);
    NdArray<T> ay = nc::zeros<T>(3, 3);
    //NdArray<T> t = nc::zeros<T>(timesteps);

    init_next_random_iteration<T>(x, y, vx, vy, ax, ay);

    if(end == 0){
        end = start + config.iterations;
    }

    size_t increment = config.iterations;
    for (size_t iteration = start; iteration < end; iteration++)
    {
        auto start = chrono::high_resolution_clock::now();

        int moment_of_failure = compute_verlet<T>(
            config.step_size,
            x,
            y,
            config.M,
            ax,
            ay,
            config.G,
            vx,
            vy);

        if (moment_of_failure == -1)
        {
            save_data<T>(to_string(iteration), config, x, y, vx, vy);
        }
        else
        {
            cout << "Run " << iteration << " failed at i= " << moment_of_failure << '\n';

            // runs that failed have only zero's at the end
            // find the point from where everything is all zero's and delete that part of the data
            NdArray<T> _x = x(nc::Slice(0, moment_of_failure), x.cSlice());
            NdArray<T> _y = y(nc::Slice(0, moment_of_failure), y.cSlice());
            NdArray<T> _vx = vx(nc::Slice(0, moment_of_failure), vx.cSlice());
            NdArray<T> _vy = vy(nc::Slice(0, moment_of_failure), vy.cSlice());

            string failure_name = "_";
            failure_name.append(to_string(iteration));

            save_data<T>(failure_name, config, _x, _y, _vx, _vy);
        }

        init_next_random_iteration<T>(x, y, vx, vy, ax, ay);
        auto end = chrono::high_resolution_clock::now();
        chrono::duration<double> duration = end - start;
        cout << "Run " << iteration << " finished in " << duration.count() << " seconds\n";


        cout << iteration << " mean vx: " << nc::mean(vx)[0] << '\n';
        cout << iteration << " max vx: " << nc::max(vx)[0] << '\n';

    }
}

int main()
{
    const int numThreads = omp_get_num_procs();

    Config<double> config = Config<double>();
    config.save();

    #pragma omp parallel for
    for(int i=0;i < numThreads; i++){
        const int start = config.iterations * i / numThreads;
        const int end = config.iterations * (i+1) / numThreads;

        generateData<double>(config, start, end);
    }

}
