use reqwest::header::{AUTHORIZATION, CONTENT_TYPE};
use reqwest::Response;
use serde_json::{json, Value};
use std::fs::File;
use std::io::{Error, Read};
use std::path::Path;
use tokio::io::AsyncReadExt;

const REQUEST_UPLOAD: &str = "https://livepeer.com/api/asset/request-upload";
const EXPORT_ASSET: &str = "https://livepeer.com/api/asset/";
const RETRIEVE_ASSET: &str = "https://livepeer.com/api/asset/";

pub struct Livepeer {
    api_key: String,
    client: reqwest::Client,
}

impl Livepeer {
    pub(crate) fn new(api_key: String) -> Self {
        Livepeer {
            api_key,
            client: reqwest::Client::new(),
        }
    }

    // pub async fn export_asset_to_ipfs(&self, asset_id: &str) -> Response {
    //     let url = format!("{}{}/export", EXPORT_ASSET, asset_id);
    //     let json_body = json!({ "ipfs": {} });
    //     self.make_post_request(&url, &json_body).await
    // }

    pub async fn retrieve_asset(&self, asset_id: &String) -> Response {
        let url = format!("{}{}", RETRIEVE_ASSET, asset_id);
        self.make_get_request(&url).await
    }

    pub async fn upload_content(
        &self,
        video_path: &Path,
        asset_url: &String,
    ) -> Result<Response, reqwest::Error> {
        let mut buf = Vec::new();

        match File::open(video_path) {
            Err(e) => println!("Error opening file"),
            Ok(mut file) => {
                file.read_to_end(&mut buf).expect("TODO: panic message");
            }
        }

        self.client
            .put(asset_url)
            .header("Content-Type", "video/mp4")
            .body(buf)
            .send()
            .await
    }

    pub async fn get_livepeer_url(&self, video_name: &str) -> Result<Response, reqwest::Error> {
        let json_body = json!({ "name": video_name });
        let response = self.make_post_request(REQUEST_UPLOAD, &json_body).await;

        response
    }

    async fn make_post_request(&self, url: &str, body: &Value) -> Result<Response, reqwest::Error> {
        self.client
            .post(url)
            .header(AUTHORIZATION, format!("Bearer {}", self.api_key))
            .header(CONTENT_TYPE, "application/json")
            .json(body)
            .send()
            .await
    }

    async fn make_get_request(&self, url: &str) -> Response {
        self.client
            .get(url)
            .header(AUTHORIZATION, format!("Bearer {}", self.api_key))
            .header(CONTENT_TYPE, "application/json")
            .send()
            .await
            .unwrap()
    }
}
