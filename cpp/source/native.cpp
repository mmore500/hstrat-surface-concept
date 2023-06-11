#include <iostream>

#include "Empirical/include/emp/base/vector.hpp"

#include "hsc/config/Config.hpp"
#include "hsc/config/setup_config_native.hpp"
#include "hsc/example.hpp"

// This is the main function for the NATIVE version of Hereditary Stratigraphic Surface Concept.

hsc::Config cfg;

int main(int argc, char* argv[]) {
  // Set up a configuration panel for native application
  setup_config_native(cfg, argc, argv);
  cfg.Write(std::cout);

  std::cout << "Hello, world!" << "\n";

  return hsc::example();
}
