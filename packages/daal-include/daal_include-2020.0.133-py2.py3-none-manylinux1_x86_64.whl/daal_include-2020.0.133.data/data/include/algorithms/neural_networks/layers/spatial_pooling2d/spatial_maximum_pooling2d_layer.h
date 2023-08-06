/* file: spatial_maximum_pooling2d_layer.h */
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

/*
//++
//  Implementation of spatial pyramid maximum 2D pooling layer.
//--
*/

#ifndef __SPATIAL_MAXIMUM_POOLING2D_LAYER_H__
#define __SPATIAL_MAXIMUM_POOLING2D_LAYER_H__

#include "algorithms/algorithm.h"
#include "data_management/data/tensor.h"
#include "services/daal_defines.h"
#include "algorithms/neural_networks/layers/layer.h"
#include "algorithms/neural_networks/layers/spatial_pooling2d/spatial_maximum_pooling2d_layer_types.h"
#include "algorithms/neural_networks/layers/spatial_pooling2d/spatial_maximum_pooling2d_layer_forward.h"
#include "algorithms/neural_networks/layers/spatial_pooling2d/spatial_maximum_pooling2d_layer_backward.h"


namespace daal
{
namespace algorithms
{
namespace neural_networks
{
namespace layers
{
/**
 * \brief Contains classes for spatial pyramid maximum two-dimensional (2D) pooling layer
 */
namespace spatial_maximum_pooling2d
{
/**
 * \brief Contains version 1.0 of Intel(R) Data Analytics Acceleration Library (Intel(R) DAAL) interface.
 */
namespace interface1
{
/**
 * @ingroup spatial_maximum_pooling2d
 * @{
 */
/**
 * <a name="DAAL-CLASS-ALGORITHMS__NEURAL_NETWORKS__LAYERS__SPATIAL_MAXIMUM_POOLING2D__BATCH"></a>
 * \brief Provides methods for the spatial pyramid maximum 2D pooling layer in the batch processing mode
 * <!-- \n<a href="DAAL-REF-SPATIAL_MAXIMUMPOOLING2DFORWARD-ALGORITHM">Forward spatial pyramid maximum 2D pooling layer description and usage models</a> -->
 * <!-- \n<a href="DAAL-REF-SPATIAL_MAXIMUMPOOLING2DBACKWARD-ALGORITHM">Backward spatial pyramid maximum 2D pooling layer description and usage models</a> -->
 *
 * \tparam algorithmFPType  Data type to use in intermediate computations for the spatial pyramid maximum 2D pooling layer, double or float
 * \tparam method           Spatial pyramid spatial pyramid maximum 2D pooling layer method, \ref Method
 *
 * \par Enumerations
 *      - \ref Method      Computation methods
 *      - \ref LayerDataId Identifiers of collection in results of forward and in input objects for the backward average 2D pooling layer
 *
 * \par References
 *      - \ref forward::interface1::Batch "forward::Batch" class
 *      - \ref backward::interface1::Batch "backward::Batch" class
 */
template<typename algorithmFPType = DAAL_ALGORITHM_FP_TYPE, Method method = defaultDense>
class Batch : public LayerIface
{
public:
    Parameter parameter; /*!< Spatial pyramid spatial pyramid maximum 2D pooling layer parameters */

    /**
     * Constructs the spatial pyramid maximum 2D pooling layer
     * \param[in] nDimensions   Number of dimensions in input gradient tensor
     * \param[in] pyramidHeight The value of pyramid height
     */
    Batch(size_t pyramidHeight, size_t nDimensions) : parameter(pyramidHeight, nDimensions - 2, nDimensions - 1)
    {
        forward::Batch<algorithmFPType, method> *forwardLayerObject = new forward::Batch<algorithmFPType, method>(parameter);
        backward::Batch<algorithmFPType, method> *backwardLayerObject = new backward::Batch<algorithmFPType, method>(parameter);

        LayerIface::forwardLayer = services::SharedPtr<forward::Batch<algorithmFPType, method> >(forwardLayerObject);
        LayerIface::backwardLayer = services::SharedPtr<backward::Batch<algorithmFPType, method> >(backwardLayerObject);
    }
};
/** @} */
} // namespace interface1
using interface1::Batch;

} // namespace spatial_maximum_pooling2d
} // namespace layers
} // namespace neural_networks
} // namespace algorithms
} // namespace daal

#endif
