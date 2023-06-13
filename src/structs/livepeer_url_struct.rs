use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Debug)]
pub struct Asset {
    pub id: String,
    #[serde(rename = "playbackId")]
    pub playback_id: Option<String>,
    #[serde(rename = "userId")]
    user_id: String,
    #[serde(rename = "createdAt")]
    created_at: u64,
    status: Status,
    name: String,
    source: Source,
}

#[derive(Serialize, Deserialize, Debug)]
struct Status {
    phase: String,
    #[serde(rename = "updatedAt")]
    updated_at: u64,
}

#[derive(Serialize, Deserialize, Debug)]
struct Source {
    #[serde(rename = "type")]
    type_: String,
}

#[derive(Serialize, Deserialize, Debug)]
struct Task {
    id: String,
}

#[derive(Serialize, Deserialize, Debug)]
pub struct Response {
    pub url: String,
    #[serde(rename = "tusEndpoint")]
    tusendpoint: String,
    pub asset: Asset,
    task: Task,
}
