#pragma once
#ifndef HSC_CONFIG_TRY_READ_CONFIG_FILE_HPP_INCLUDE
#define HSC_CONFIG_TRY_READ_CONFIG_FILE_HPP_INCLUDE

#include <cstdlib>
#include <filesystem>
#include <iostream>

#include "Config.hpp"

namespace hsc {

void try_read_config_file(hsc::Config & config, emp::ArgManager & am) {
  if(std::filesystem::exists("hsc.cfg")) {
    std::cout << "Configuration read from hsc.cfg" << '\n';
    config.Read("hsc.cfg");
  }
  am.UseCallbacks();
  if (am.HasUnused())
    std::exit(EXIT_FAILURE);
}

} // namespace hsc

#endif // #ifndef HSC_CONFIG_TRY_READ_CONFIG_FILE_HPP_INCLUDE
