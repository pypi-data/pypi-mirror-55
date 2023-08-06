/* file: locallyconnected2d_layer.h */
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
//  Implementation of two-dimensional (2D) locally connected neural network layer.
//--
*/

#ifndef __LOCALLYCONNECTED2D_LAYER_H__
#define __LOCALLYCONNECTED2D_LAYER_H__

#include "algorithms/algorithm.h"
#include "data_management/data/tensor.h"
#include "services/daal_defines.h"
#include "algorithms/neural_networks/layers/layer.h"
#include "algorithms/neural_networks/layers/locallyconnected2d/locallyconnected2d_layer_types.h"
#include "algorithms/neural_networks/layers/locallyconnected2d/locallyconnected2d_layer_forward.h"
#include "algorithms/neural_networks/layers/locallyconnected2d/locallyconnected2d_layer_backward.h"

namespace daal
{
namespace algorithms
{
namespace neural_networks
{
namespace layers
{
/**
 * \brief Contains classes for neural network 2D locally connected layer
 */
namespace locallyconnected2d
{
/**
 * \brief Contains version 1.0 of Intel(R) Data Analytics Acceleration Library (Intel(R) DAAL) interface.
 */
namespace interface1
{
/**
 * @ingroup locallyconnected2d
 * @{
 */
/**
 * <a name="DAAL-CLASS-ALGORITHMS__NEURAL_NETWORKS__LAYERS__LOCALLYCONNECTED2D__BATCH"></a>
 * \brief Computes the result of the forward and backward 2D locally connected layer of neural network in the batch processing mode
 * <!-- \n<a href="DAAL-REF-LOCALLYCONNECTED2DFORWARD-ALGORITHM">Forward 2D locally connected layer description and usage models</a> -->
 * <!-- \n<a href="DAAL-REF-LOCALLYCONNECTED2DBACKWARD-ALGORITHM">Backward 2D locally connected layer description and usage models</a> -->
 *
 * \tparam algorithmFPType Data type to use in intermediate computations for the 2D locally connected layer, double or float
 * \tparam method          Batch 2D locally connected layer computation method, \ref Method
 *
 * \par References
 *      - \ref forward::interface1::Batch  "forward::Batch" class
 *      - \ref backward::interface1::Batch "backward::Batch" class
 */
template<typename algorithmFPType = DAAL_ALGORITHM_FP_TYPE, Method method = defaultDense>
class Batch : public LayerIface
{
public:
    Parameter parameter; /*!< %Parameters of the layer */

    /** Default constructor */
    Batch()
    {
        forward::Batch<algorithmFPType, method> *forwardLayerObject = new forward::Batch<algorithmFPType, method>(parameter);
        backward::Batch<algorithmFPType, method> *backwardLayerObject = new backward::Batch<algorithmFPType, method>(parameter);

        LayerIface::forwardLayer = services::SharedPtr<forward::Batch<algorithmFPType, method> >(forwardLayerObject);
        LayerIface::backwardLayer = services::SharedPtr<backward::Batch<algorithmFPType, method> >(backwardLayerObject);
    };
};
/** @} */
} // namespace interface1
using interface1::Batch;

} // namespace locallyconnected2d
} // namespace layers
} // namespace neural_networks
} // namespace algorithms
} // namespace daal
#endif
