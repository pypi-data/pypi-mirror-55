/* file: conversion.h */
/*******************************************************************************
* Copyright 2014-2019 Intel Corporation
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
*     http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*******************************************************************************/

#ifndef __DATA_MANAGEMENT_DATA_INTERNAL_CONVERSION_H__
#define __DATA_MANAGEMENT_DATA_INTERNAL_CONVERSION_H__

#include "data_management/features/defines.h"

namespace daal
{
namespace data_management
{
namespace internal
{

/* Renamed from InternalNumType */
enum ConversionDataType
{
    DAAL_SINGLE = 0,
    DAAL_DOUBLE = 1,
    DAAL_INT32  = 2,
    DAAL_OTHER  = 0xfffffff
};

/**
 * \return Internal numeric type
 */
template<typename T>
inline ConversionDataType getConversionDataType()          { return DAAL_OTHER;  }
template<>
inline ConversionDataType getConversionDataType<int>()     { return DAAL_INT32;  }
template<>
inline ConversionDataType getConversionDataType<double>()  { return DAAL_DOUBLE; }
template<>
inline ConversionDataType getConversionDataType<float>()   { return DAAL_SINGLE; }


typedef void(*vectorConvertFuncType)(size_t n, const void *src,
                                               void *dst);

typedef void(*vectorStrideConvertFuncType)(size_t n, const void *src, size_t srcByteStride,
                                                     void *dst, size_t dstByteStride);

DAAL_EXPORT vectorConvertFuncType getVectorUpCast(int, int);
DAAL_EXPORT vectorConvertFuncType getVectorDownCast(int, int);

DAAL_EXPORT vectorStrideConvertFuncType getVectorStrideUpCast(int, int);
DAAL_EXPORT vectorStrideConvertFuncType getVectorStrideDownCast(int, int);

#define DAAL_REGISTER_WITH_HOMOGEN_NT_TYPES(FUNC) \
FUNC(float)                                       \
FUNC(double)                                      \
FUNC(int)                                         \
FUNC(unsigned int)                                \
FUNC(DAAL_INT64)                                  \
FUNC(DAAL_UINT64)                                 \
FUNC(char)                                        \
FUNC(unsigned char)                               \
FUNC(short)                                       \
FUNC(unsigned short)                              \
FUNC(long)                                        \
FUNC(unsigned long)

template<typename T> DAAL_EXPORT void vectorAssignValueToArray(T* const ptr, const size_t n, const T value);

} // namespace internal
} // namespace data_management
} // namespace daal

#endif
