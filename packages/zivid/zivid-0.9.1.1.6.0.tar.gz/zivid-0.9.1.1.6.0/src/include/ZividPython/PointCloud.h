#pragma once

#include <Zivid/PointCloud.h>
#include <ZividPython/Wrappers.h>

namespace ZividPython
{
    void wrapClass(pybind11::class_<Zivid::PointCloud> pyClass);
} // namespace ZividPython
