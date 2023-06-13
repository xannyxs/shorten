use crate::livepeer::Livepeer;
use crate::structs::{livepeer_url_struct, retrieve_asset_struct};
use crate::upload_video::call_python_script;
use mime_guess::from_path;
use reqwest::Response as ReqwestResponse;
use std::io::{Error, ErrorKind};
use std::path::Path;
use tokio::time::Duration;

const MAX_TIMEOUT: i32 = 600;
const SLEEP_INTERVAL: i32 = 20;

async fn video_is_processed(livepeer: &Livepeer, asset_id: &String) -> Result<String, Error> {
    let mut asset: ReqwestResponse = livepeer.retrieve_asset(asset_id).await;
    let mut elapsed_time = 0;

    while elapsed_time < MAX_TIMEOUT {
        println!("Waiting for 'playbackUrl' to be available...");

        let body = asset.text().await;
        let parsed_body = match body {
            Ok(text) => {
                match serde_json::from_str::<retrieve_asset_struct::Response>(text.as_str()) {
                    Ok(data) => Ok(data),
                    Err(e) => Err(Error::new(ErrorKind::InvalidInput, e)),
                }
            }
            Err(_) => Err(Error::new(
                ErrorKind::InvalidInput,
                "Could not parse body. Did Livepeer return anything?",
            )),
        };

        if let Ok(parsed_body) = parsed_body {
            if let Some(playback_url) = parsed_body.playback_url {
                return Ok(playback_url);
            }
        }

        tokio::time::sleep(Duration::from_secs(SLEEP_INTERVAL as u64)).await; // async sleep
        elapsed_time += SLEEP_INTERVAL;

        asset = livepeer.retrieve_asset(asset_id).await;
    }

    Err(Error::new(ErrorKind::TimedOut, "Request Timeout"))
}

fn is_video_file(video_path: &Path) -> bool {
    let mime = from_path(video_path).first_or_octet_stream();

    mime.type_().as_str().starts_with("video")
}

pub async fn process_file(livepeer: &Livepeer, video_path: &Path) -> Result<(), Error> {
    println!("{}", video_path.display());

    if !video_path.exists() {
        return Err(Error::new(ErrorKind::InvalidInput, "File does not exist"));
    }
    if !is_video_file(video_path) {
        return Err(Error::new(ErrorKind::InvalidInput, "File is not a video"));
    }

    let file_name = video_path
        .file_name()
        .and_then(|name| name.to_str())
        .ok_or_else(|| {
            Error::new(
                ErrorKind::Other,
                format!("Invalid filename: {:?}", video_path.file_name().unwrap()),
            )
        })?;

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
        Ok(text) => match serde_json::from_str::<livepeer_url_struct::Response>(&text) {
            Ok(data) => Ok(data),
            Err(e) => Err(Error::new(ErrorKind::Other, e)),
        },
        Err(e) => Err(Error::new(ErrorKind::Other, e)),
    };

    let parsed_body = match parsed_body {
        Ok(parsed_body) => parsed_body,
        Err(e) => return Err(e),
    };

    livepeer
        .upload_content(video_path, &parsed_body.url)
        .await
        .map_err(|_| Error::new(ErrorKind::TimedOut, "Upload content failed"))?;

    let playback_url = video_is_processed(livepeer, &parsed_body.asset.id).await?;

    call_python_script(video_path, &playback_url).map_err(|_| {
        Error::new(
            ErrorKind::Interrupted,
            "Something went wrong in the python script",
        )
    })?;

    Ok(())
}
