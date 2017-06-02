/*
 * <one line to give the library's name and an idea of what it does.>
 * Copyright (C) 2017  Aetf <aetf@unlimitedcodeworks.xyz>
 * 
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * 
 */

#ifndef TFSESSION_H
#define TFSESSION_H

#include "executor.pb.h"
#include "tfoplibrary.pb.h"

#include <tensorflow/core/framework/op_segment.h>
#include <tensorflow/core/framework/op_kernel.h>
#include <tensorflow/core/framework/resource_mgr.h>
#include <tensorflow/core/framework/allocator.h>
#include <tensorflow/core/util/tensor_slice_reader_cache.h>
#include <tensorflow/core/platform/mutex.h>

#include <memory>
#include <mutex>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

typedef tensorflow::gtl::InlinedVector<tensorflow::TensorValue, 4> TensorValueVec;
typedef tensorflow::gtl::InlinedVector<tensorflow::DeviceContext*, 4> DeviceContextVec;
typedef tensorflow::gtl::InlinedVector<tensorflow::AllocatorAttributes, 4> AllocatorAttributeVec;

namespace tensorflow {
class OptimizerOptions;
class NodeDef;
class FunctionDefLibrary;
class ConfigProto;
}

class TFDevice;
class TFSession;
class TFOpLibrary;
class TFRendezvous;

class TFContext
{
public:
    TFContext();
    ~TFContext();

    tensorflow::OpKernelContext *ctx();

    void FillOutputAttrs();

    tensorflow::ScopedStepContainer step_container;
    tensorflow::checkpoint::TensorSliceReaderCacheWrapper slice_reader_cache_wrapper;

    TensorValueVec inputs;

    DeviceContextVec input_device_contexts;
    AllocatorAttributeVec input_alloc_attrs;
    tensorflow::mutex ref_mutex;

    std::vector<tensorflow::AllocatorAttributes> output_attrs;

    tensorflow::OpKernelContext::Params params;
private:
    std::unique_ptr<tensorflow::OpKernelContext> context;
};

class TFSession
{
public:
    TFSession(TFOpLibrary *opLibrary, const tensorflow::FunctionDefLibrary &fDefLib,
              int graphDefVersion, const tensorflow::OptimizerOptions &optimizerOpts);

    ~TFSession();

    std::unique_ptr<tensorflow::OpKernel> createKernel(const tensorflow::NodeDef &nodedef);

    std::unique_ptr<TFContext> createContext(const executor::TFOpContextDef &tfdef, tensorflow::OpKernel *opkernel);

    void registerTensorMemory(const tensorflow::Tensor &tensor);
    tensorflow::Tensor *tensorFromAddrHandle(uint64_t addr_handle);
    tensorflow::Tensor *findTensorFromProto(const tensorflow::TensorProto &proto);

    // convinence method that combines create a tensor from proto, allocate and fill in memory,
    // and finally register
    void createAndRegister(const tensorflow::TensorProto &proto);

    void tensorToProto(tensorflow::TensorProto *proto, const tensorflow::Tensor &tensor);

private:
    void registerTensorMemoryLocked(tensorflow::Tensor *tensor);

    TFOpLibrary *m_oplibrary;

    std::string m_sessHandle;
    tensorflow::OpSegment m_opseg;

    tensorflow::FunctionLibraryDefinition m_flibDef;
    std::unique_ptr<tensorflow::FunctionLibraryRuntime> m_fruntime;
    std::unique_ptr<TFDevice> m_device;
    std::unique_ptr<TFRendezvous> m_rendez;

    tensorflow::mutex m_mu;
    std::unordered_map<uint64_t, tensorflow::Tensor*> m_tensors;
};

#endif // TFSESSION_H