//
// Created by Xander Voorvaart on 22/05/2023.
//

#define CATCH_CONFIG_MAIN
#include "videoProcessing.hpp"
#include "catch2/catch_test_macros.hpp"

TEST_CASE("Test processFile", "[livepeer]") {
	Livepeer livepeer;

	SECTION("Processing with error") {
		REQUIRE_THROWS(processFile(livepeer, "file_does_not_exist"));
	}
}
