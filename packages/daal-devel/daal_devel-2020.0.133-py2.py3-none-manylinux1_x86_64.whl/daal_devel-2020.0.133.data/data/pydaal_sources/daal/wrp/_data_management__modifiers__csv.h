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


#ifndef SWIG_csv_WRAP_H_
#define SWIG_csv_WRAP_H_

#include <map>
#include <string>


class SwigDirector_FeatureModifier : public daal::data_management::modifiers::csv::interface1::PyFeatureModifier, public Swig::Director {

public:
    SwigDirector_FeatureModifier(PyObject *self, size_t noof = 0, size_t nor = 1);
    virtual ~SwigDirector_FeatureModifier();
    virtual void initialize(daal::data_management::modifiers::csv::interface1::Config &config);
    virtual void initializeSwigPublic(daal::data_management::modifiers::csv::interface1::Config &config) {
      daal::data_management::modifiers::csv::interface1::PyFeatureModifier::initialize(config);
    }
    virtual void finalize(daal::data_management::modifiers::csv::interface1::Config &config);
    virtual void finalizeSwigPublic(daal::data_management::modifiers::csv::interface1::Config &config) {
      daal::data_management::modifiers::csv::interface1::PyFeatureModifier::finalize(config);
    }
    virtual size_t getNumberOfOutputFeatures();
    virtual PyObject *apply(PyObject *tokens);
    virtual void apply(daal::data_management::modifiers::csv::interface1::Context &context);
    virtual void applySwigPublic(daal::data_management::modifiers::csv::interface1::Context &context) {
      daal::data_management::modifiers::csv::interface1::PyFeatureModifier::apply(context);
    }

/* Internal director utilities */
public:
    bool swig_get_inner(const char *swig_protected_method_name) const {
      std::map<std::string, bool>::const_iterator iv = swig_inner.find(swig_protected_method_name);
      return (iv != swig_inner.end() ? iv->second : false);
    }
    void swig_set_inner(const char *swig_protected_method_name, bool swig_val) const {
      swig_inner[swig_protected_method_name] = swig_val;
    }
private:
    mutable std::map<std::string, bool> swig_inner;

#if defined(SWIG_PYTHON_DIRECTOR_VTABLE)
/* VTable implementation */
    PyObject *swig_get_method(size_t method_index, const char *method_name) const {
      PyObject *method = vtable[method_index];
      if (!method) {
        swig::SwigVar_PyObject name = SWIG_Python_str_FromChar(method_name);
        method = PyObject_GetAttr(swig_get_self(), name);
        if (!method) {
          std::string msg = "Method in class FeatureModifier doesn't exist, undefined ";
          msg += method_name;
          Swig::DirectorMethodException::raise(msg.c_str());
        }
        vtable[method_index] = method;
      }
      return method;
    }
private:
    mutable swig::SwigVar_PyObject vtable[2];
#endif

};


#endif
