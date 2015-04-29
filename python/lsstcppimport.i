/*
 * LSST Data Management System
 * Copyright 2008-2013 LSST Corporation.
 *
 * This product includes software developed by the
 * LSST Project (http://www.lsst.org/).
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
 * You should have received a copy of the LSST License Statement and
 * the GNU General Public License along with this program.  If not,
 * see <http://www.lsstcorp.org/LegalNotices/>.
 */

%module lsstcppimport

%{
#include "lsst/base/ModuleImporter.h"

namespace lsst { namespace base {

class PythonModuleImporter : public ModuleImporter {
public:
    static ModuleImporter const * get() {
        static PythonModuleImporter const instance;
        return &instance;
    }
private:
    PythonModuleImporter() {}
protected:
    virtual bool _import(std::string const & name) const;
};

bool PythonModuleImporter::_import(std::string const & name) const {
    PyObject * mod = PyImport_ImportModule(name.c_str());
    if (mod) {
        Py_DECREF(mod);
        return true;
    } else {
        // If the Python C API call returned a null pointer, it will
        // also have set an exception.  We don't want that, because
        // this isn't necessarily an error (that's up to the caller).
        PyErr_Clear();
    }
    return false;
}

void installPythonModuleImporter() {
    ModuleImporter::install(PythonModuleImporter::get());
}

}} // namespace lsst::base
%}

%init %{
    lsst::base::installPythonModuleImporter();
%}
