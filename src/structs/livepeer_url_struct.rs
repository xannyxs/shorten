use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Debug)]
pub struct Asset {
    pub id: String,
    pub playbackId: Option<String>,
    userId: String,
    createdAt: u64,
    status: Status,
    name: String,
    source: Source,
}

#[derive(Serialize, Deserialize, Debug)]
struct Status {
    phase: String,
    updatedAt: u64,
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
    tusEndpoint: String,
    pub asset: Asset,
    task: Task,
}
