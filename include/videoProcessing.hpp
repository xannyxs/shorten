//
// Created by Xander Voorvaart on 22/05/2023.
//

#ifndef SHORTEN_VIDEOPROCESSING_HPP
#define SHORTEN_VIDEOPROCESSING_HPP

#include <string>
#include "Livepeer.hpp"

std::string videoIsProcessed(Livepeer&, const std::string&);

void processFile(Livepeer&, const std::filesystem::path&);

#endif //SHORTEN_VIDEOPROCESSING_HPP
