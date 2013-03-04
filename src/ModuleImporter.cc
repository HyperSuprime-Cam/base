// -*- lsst-c++ -*-

#include "lsst/base/ModuleImporter.h"

namespace lsst { namespace base {

namespace {

class PlaceholderModuleImporter : public ModuleImporter {
public:
    static ModuleImporter const * get() {
        static PlaceholderModuleImporter const instance;
        return &instance;
    }
private:
    PlaceholderModuleImporter() {}
protected:
    virtual bool _import(std::string const & name) const { return false; }
};

ModuleImporter const * & getImporterSingleton() {
    static ModuleImporter const * instance = PlaceholderModuleImporter::get();
    return instance;
}

} // anonymous

bool ModuleImporter::import(std::string const & name) {
    return getImporterSingleton()->_import(name);
}

void ModuleImporter::install(ModuleImporter const * importer) {
    getImporterSingleton() = importer;
}

}} // namespace lsst::base
