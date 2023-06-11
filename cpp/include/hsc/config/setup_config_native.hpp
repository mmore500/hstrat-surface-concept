#pragma once
#ifndef HSC_CONFIG_SETUP_CONFIG_NATIVE_HPP_INCLUDE
#define HSC_CONFIG_SETUP_CONFIG_NATIVE_HPP_INCLUDE

#include "Empirical/include/emp/config/ArgManager.hpp"

#include "try_read_config_file.hpp"

namespace hsc {

void setup_config_native(hsc::Config & config, int argc, char* argv[]) {
  auto specs = emp::ArgManager::make_builtin_specs(&config);
  emp::ArgManager am(argc, argv, specs);
  hsc::try_read_config_file(config, am);
}

} // namespace hsc

#endif // #ifndef HSC_CONFIG_SETUP_CONFIG_NATIVE_HPP_INCLUDE
