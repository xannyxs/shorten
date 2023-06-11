use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct Response {
    id: String,
    #[serde(rename = "hash")]
    hash: Option<Vec<Hash>>,
    name: String,
    size: Option<u64>,
    source: Source,
    status: Status,
    #[serde(rename = "userId")]
    user_id: String,
    #[serde(rename = "createdAt")]
    created_at: u64,
    #[serde(rename = "videoSpec")]
    video_spec: Option<VideoSpec>,
    #[serde(rename = "playbackId")]
    pub playback_id: String,
    #[serde(rename = "playbackurl")]
    pub playback_url: Option<String>,
    #[serde(rename = "downloadUrl")]
    pub download_url: Option<String>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Hash {
    hash: String,
    algorithm: String,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Source {
    #[serde(rename = "type")]
    type_: String,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Status {
    phase: String,
    #[serde(rename = "updatedAt")]
    updated_at: u64,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct VideoSpec {
    format: String,
    duration: f64,
}
