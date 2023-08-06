/* file: maximum_pooling1d_layer.h */
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
//  Implementation of maximum 1D pooling layer.
//--
*/

#ifndef __MAXIMUM_POOLING1D_LAYER_H__
#define __MAXIMUM_POOLING1D_LAYER_H__

#include "algorithms/algorithm.h"
#include "data_management/data/tensor.h"
#include "services/daal_defines.h"
#include "algorithms/neural_networks/layers/layer.h"
#include "algorithms/neural_networks/layers/pooling1d/maximum_pooling1d_layer_types.h"
#include "algorithms/neural_networks/layers/pooling1d/maximum_pooling1d_layer_forward.h"
#include "algorithms/neural_networks/layers/pooling1d/maximum_pooling1d_layer_backward.h"


namespace daal
{
namespace algorithms
{
namespace neural_networks
{
namespace layers
{
/**
 * \brief Contains classes for maximum one-dimensional (1D) pooling layer
 */
namespace maximum_pooling1d
{
namespace interface1
{
/**
 * @ingroup maximum_pooling1d
 * @{
 */
/**
 * <a name="DAAL-CLASS-ALGORITHMS__NEURAL_NETWORKS__LAYERS__MAXIMUM_POOLING1D__BATCH"></a>
 * \brief Provides methods for the maximum 1D pooling layer in the batch processing mode
 * <!-- \n<a href="DAAL-REF-MAXIMUMPOOLING1DFORWARD-ALGORITHM">Forward maximum 1D pooling layer description and usage models</a> -->
 * <!-- \n<a href="DAAL-REF-MAXIMUMPOOLING1DBACKWARD-ALGORITHM">Backward maximum 1D pooling layer description and usage models</a> -->
 *
 * \tparam algorithmFPType  Data type to use in intermediate computations for the maximum 1D pooling layer, double or float
 * \tparam method           Maximum 1D pooling layer method, \ref Method
 *
 * \par Enumerations
 *      - \ref Method      Computation methods
 *      - \ref LayerDataId Identifiers of collection in results of forward and in input objects for the backward average 1D pooling layer
 *
 * \par References
 *      - \ref forward::interface1::Batch "forward::Batch" class
 *      - \ref backward::interface1::Batch "backward::Batch" class
 */
template<typename algorithmFPType = DAAL_ALGORITHM_FP_TYPE, Method method = defaultDense>
class Batch : public LayerIface
{
public:
    Parameter parameter; /*!< Maximum 1D pooling layer parameters */
    /**
     * Constructs the maximum 1D pooling layer
     * \param[in] nDimensions Number of dimensions in input gradient tensor
     */
    Batch(size_t nDimensions) : parameter(nDimensions - 1)
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

} // namespace maximum_pooling1d
} // namespace layers
} // namespace neural_networks
} // namespace algorithms
} // namespace daal

#endif
