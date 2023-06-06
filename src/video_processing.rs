use crate::json_deserialize;
use crate::json_deserialize::Response;
use crate::livepeer::Livepeer;
use crate::upload_video::call_python_script;
use mime_guess::from_path;
use reqwest::Error as ReqwestError;
use reqwest::Response as ReqwestResponse;
use serde_json::json;
use std::io::Error;
use std::path::Path;
use std::{io, process};
use tokio::time::Duration;

const MAX_TIMEOUT: i32 = 600;
const SLEEP_INTERVAL: i32 = 20;

async fn video_is_processed(livepeer: &Livepeer, asset_id: &String) -> Result<String, Error> {
    let mut asset: ReqwestResponse = livepeer.retrieve_asset(asset_id).await;
    let mut elapsed_time = 0;

    while elapsed_time < MAX_TIMEOUT {
        println!("Waiting for 'playbackUrl' to be available...");

        let body = asset.text().await;
        let parsed_body = match &body {
            Ok(text) => match serde_json::from_str::<json_deserialize::Response>(text) {
                Ok(data) => {
                    println!("Asset ID: {}", data.asset.id);
                    Ok(data)
                }
                Err(_) => Err("Failed to deserialize JSON"),
            },
            Err(e) => {
                eprintln!("{}", e);
                Err("Failed to get the response body")
            }
        };

        if let Some(playback_url) = parsed_body.unwrap().asset.playbackId {
            return Ok(playback_url);
        }

        tokio::time::sleep(Duration::from_secs(SLEEP_INTERVAL as u64)).await; // async sleep
        elapsed_time += SLEEP_INTERVAL;

        asset = livepeer.retrieve_asset(asset_id).await;
    }

    Err(std::io::Error::new(
        io::ErrorKind::TimedOut,
        "Request Timeout",
    ))
}

fn is_video_file(video_path: &Path) -> bool {
    let mime = from_path(video_path).first_or_octet_stream();

    mime.type_().as_str().starts_with("video")
}

pub async fn process_file(livepeer: &Livepeer, video_path: &Path) -> Result<(), reqwest::Error> {
    println!("{}", video_path.display());

    if !video_path.exists() {
        eprintln!("File does not exist");
        process::exit(1);
    }
    if !is_video_file(video_path) {
        eprintln!("File is not a video");
        process::exit(1);
    }

    let file_name = video_path
        .file_name()
        .and_then(|name| name.to_str())
        .unwrap_or_else(|| panic!("Invalid filename: {:?}", video_path.file_name().unwrap()));

    let body: Result<String, String> = match livepeer.get_livepeer_url(file_name).await {
        Err(e) => Err(format!("Failed to get Livepeer URL: {}", e)),
        Ok(response) => match response.status() {
            reqwest::StatusCode::OK => {
                println!("OK");
                response
                    .text()
                    .await
                    .map_err(|e| format!("Failed to get response text: {}", e))
            }
            reqwest::StatusCode::UNAUTHORIZED => {
                let err_msg = "Token unauthorized";
                println!("{}", err_msg);
                Err(err_msg.to_string())
            }
            _ => {
                let err_msg = "A fatal error";
                println!("{}", err_msg);
                Err(err_msg.to_string())
            }
        },
    };

    let parsed_body = match body {
        Ok(text) => match serde_json::from_str::<json_deserialize::Response>(&text) {
            Ok(data) => Ok(data),
            Err(_) => Err(std::io::Error::new(
                std::io::ErrorKind::Other,
                "Failed to deserialize JSON",
            )),
        },
        Err(e) => {
            eprintln!("{}", e);
            Err(std::io::Error::new(
                std::io::ErrorKind::Other,
                "Failed to get the response body",
            ))
        }
    };

    if let Ok(parsed_body) = &parsed_body {
        livepeer
            .upload_content(video_path, &parsed_body.url)
            .await
            .expect("TODO: panic message");

        let playback_url = video_is_processed(livepeer, &parsed_body.asset.id).await;
    }

    // call_python_script(video_path, &playback_url)
    Ok(())
}
