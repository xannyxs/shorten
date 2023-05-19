//
// Created by Xander Voorvaart on 13/05/2023.
//

#include "videoFormatting.hpp"
#include "catch2/catch_test_macros.hpp"

#include <string>

TEST_CASE("Test checkFile function") {
	REQUIRE_THROWS_AS(checkFile("non_existent_file.txt"), std::runtime_error);
	// Exists, but it is the wrong path
	REQUIRE_THROWS(checkFile("test.mov"));
	// Existing file, but it is not a video
	REQUIRE_THROWS_AS(checkFile("existing_file.txt"), std::runtime_error);
	REQUIRE_NOTHROW(checkFile("/Users/xander/Desktop/shorten/tests/test_files/test.mov"));
}

// Note: We're not writing tests for isVideoFile as it's not practical to test it
// without a proper video file or a way to mock the libmagic library.
