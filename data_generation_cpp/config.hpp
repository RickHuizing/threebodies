#ifndef CONFIG_HPP
#define CONFIG_HPP

#include <NumCpp.hpp>
#include <string>
#include <fstream>

template <typename T>
class Config
{
public:
    // name of the configuration, used as folder name while saving results
    std::string name = "default";

    // time parameters. Default is from t0 to t5, with steps of 0.001. Result is a dataset of 5000 time steps
    T time_end = 5;
    T step_size = 0.000001;

    size_t iterations = 10;

    // Body mass
    T m1 = 1;
    T m2 = 1;
    T m3 = 1;
    nc::NdArray<T> M;

    // Newton constant
    T G = 1;

    Config()
    {
        M = nc::NdArray<T>(1, 3);
        M[0] = m1;
        M[1] = m2;
        M[2] = m3;
    }

    nc::NdArray<T> time_vector()
    {
        return nc::arange<T>(0, time_end, step_size);
    }

    std::string get_path()
    {
        std::string path = "results/";
        path.append(name);
        path.append("/");
        return path;
    }

    void save(){
        std::string path = "results/";
        path.append(name);
        path.append("/config.json"); // Not actually sure if it meets json standard
        std::ofstream outfile(path);
        outfile << "{\n";

        outfile << "\t\"name\": \"" << name << "\",\n";
        outfile << "\t\"time_end\": " << time_end << ",\n";
        outfile << "\t\"step_size\": " << step_size << ",\n";
        outfile << "\t\"iterations\": " << iterations << ",\n";

        outfile << "\t \"m1\": " << m1 << ",\n";
        outfile << "\t \"m2\": " << m2 << ",\n";
        outfile << "\t \"m3\": " << m3 << ",\n";
        outfile << "\t \"G\": " << G << "\n";

        outfile << "}";
        outfile.close(); 
    }
};

#endif