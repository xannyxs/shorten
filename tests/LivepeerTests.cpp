#define CATCH_CONFIG_MAIN
#include "Livepeer.hpp"
#include "catch2/catch_test_macros.hpp"

#include <iostream>

#define ASSETID "4fc8afe5-8299-45e4-b21f-ab57e9b44626"

TEST_CASE("Testing Livepeer class") {
	Livepeer livepeer;

	SECTION("Export asset to IPFS") {
		nlohmann::json response = livepeer.exportAssetToIPFS(ASSETID);

		REQUIRE(response.contains("task"));
		REQUIRE(response["task"]["type"] == "export");
		REQUIRE(response["task"]["inputAssetId"] == ASSETID);
	}

	SECTION("Retrieve asset") {
		nlohmann::json response = livepeer.retrieveAsset(ASSETID);

		REQUIRE(response.contains("id"));
		REQUIRE(response["id"] == ASSETID);
	}

	SECTION("Upload content") {
		std::string filePath = "test.mp4";
		std::string assetURL = "https://livepeer.com/api/asset/upload";

		REQUIRE_THROWS(livepeer.uploadContent(filePath, assetURL));
	}

	SECTION("Get Livepeer URL") {
		std::string videoName = "testVideo";
		nlohmann::json response = livepeer.getLivepeerUrl(videoName);

		REQUIRE(response.contains("url"));
		REQUIRE(response["url"].is_string());
	}
}
