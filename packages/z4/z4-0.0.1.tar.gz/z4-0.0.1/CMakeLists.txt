cmake_minimum_required(VERSION 2.8.12)
project(z4)

add_subdirectory(pybind11)
pybind11_add_module(z4 src/main.cpp)
