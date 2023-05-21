//
// Created by Xander Voorvaart on 20/05/2023.
//

#include "Livepeer.hpp"

size_t writeCallback(void* contents, size_t size, size_t nmemb, std::string* s) {
	size_t newLength = size * nmemb;
	try {
		s->resize(s->size() + newLength);
	} catch (std::bad_alloc &e) {
		// handle memory problem
		return 0;
	}

	std::copy((char*)contents, (char*)contents + newLength, s->begin() + s->size() - newLength);
	return newLength;
}

size_t readCallback(void* ptr, std::streamsize size, size_t nmemb, void* stream) {
	auto* in = static_cast<std::ifstream*>(stream);

	in->read(static_cast<char*>(ptr), size * nmemb);
	return in->gcount();
}

std::string Livepeer::exportAssetToIPFS(const std::string& assetID) {
	CURL* curl;
	CURLcode res;
	std::string readBuffer;

	const std::string url = EXPORT_ASSET + assetID + "/export";
	const std::string json = R"({"ipfs": {}})";

	curl = curl_easy_init();

	if (!curl) {
		throw std::runtime_error("Could not initiate curl");
	}

	struct curl_slist* headers = nullptr;
	curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
	curl_easy_setopt(curl, CURLOPT_POSTFIELDS, json.c_str());

	headers = curl_slist_append(headers, ("Authorization: Bearer " + this->APIKEY).c_str());
	headers = curl_slist_append(headers, "Content-Type: application/json");
	curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);

	curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, writeCallback);
	curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);

	res = curl_easy_perform(curl);

	if (res != CURLE_OK) {
		const std::string strError = std::string("curl_easy_perform() failed:\n") + curl_easy_strerror(res);

		curl_easy_cleanup(curl);
		curl_slist_free_all(headers);

		throw std::runtime_error(strError);
	}

	curl_slist_free_all(headers);
	curl_easy_cleanup(curl);

	return readBuffer;
}

nlohmann::json Livepeer::retrieveAsset(const std::string& assetID) {
	CURL* curl;
	CURLcode res;
	std::string responseString;

	const std::string url = RETRIEVE_ASSET + assetID;
	const std::string authHeader = std::string("Authorization: Bearer ") + std::getenv("LIVEPEER_API_KEY");
	curl_global_init(CURL_GLOBAL_DEFAULT);

	curl = curl_easy_init();
	if (!curl) {
		curl_global_cleanup();
		throw std::runtime_error("Could not initiate curl");
	}

	struct curl_slist* headers = nullptr;
	headers = curl_slist_append(headers, authHeader.c_str());
	curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);

	curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
	curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, writeCallback);
	curl_easy_setopt(curl, CURLOPT_WRITEDATA, &responseString);

	res = curl_easy_perform(curl);
	if (res != CURLE_OK) {
		std::string strError = "curl_easy_perform() failed: " + std::string(curl_easy_strerror(res));
		curl_easy_cleanup(curl);
		curl_slist_free_all(headers);
		curl_global_cleanup();
		throw std::runtime_error(strError);
	}

	curl_easy_cleanup(curl);
	curl_slist_free_all(headers);
	curl_global_cleanup();

	return nlohmann::json::parse(responseString);
}

void Livepeer::uploadContent(const std::string& filePath, const std::string& assetURL) {
	CURL* curl;
	CURLcode res;

	std::ifstream fileStream(filePath, std::ios::binary);

	if (!fileStream) {
		throw std::runtime_error("Error opening file");
	}

	curl = curl_easy_init();

	if (!curl) {
		throw std::runtime_error("Could not initiate curl");
	}

	struct curl_slist* headers = nullptr;
	headers = curl_slist_append(headers, "Content-Type: video/mp4");

	curl_easy_setopt(curl, CURLOPT_URL, assetURL.c_str());
	curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
	curl_easy_setopt(curl, CURLOPT_UPLOAD, 1L);
	curl_easy_setopt(curl, CURLOPT_READDATA, &fileStream);
	curl_easy_setopt(curl, CURLOPT_READFUNCTION, readCallback);

	res = curl_easy_perform(curl);

	if (res != CURLE_OK) {
		const std::string strError = std::string("curl_easy_perform() failed:\n") + curl_easy_strerror(res);

		throw std::runtime_error(strError);
	}

	curl_slist_free_all(headers);
	curl_easy_cleanup(curl);
}

nlohmann::json Livepeer::getLivepeerUrl(const std::string& videoName) {
	CURL* curl;
	CURLcode res;
	std::string readBuffer;
	std::string json = R"({"name":")" + videoName + "\"}";

	curl_global_init(CURL_GLOBAL_DEFAULT);
	curl = curl_easy_init();
	if (!curl) {

		throw std::runtime_error("Could not initiate curl");
	}

	struct curl_slist* headers = nullptr;

	curl_easy_setopt(curl, CURLOPT_URL, REQUEST_UPLOAD);
	curl_easy_setopt(curl, CURLOPT_POSTFIELDS, json.c_str());

	headers = curl_slist_append(headers, ("Authorization: Bearer " + this->APIKEY).c_str());
	headers = curl_slist_append(headers, "Content-Type: application/json");
	curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);

	curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, writeCallback);
	curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);

	res = curl_easy_perform(curl);

	if (res != CURLE_OK) {
		const std::string strError = std::string("curl_easy_perform() failed:\n") + curl_easy_strerror(res);

		throw std::runtime_error(strError);
	}

	curl_slist_free_all(headers);
	curl_easy_cleanup(curl);

	return nlohmann::json::parse(readBuffer);
}

