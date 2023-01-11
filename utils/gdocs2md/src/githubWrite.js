const { Octokit } = require("@octokit/rest");
const { Base64 } = require("js-base64");
const { GITHUB_TOKEN, GITHUB_NAME, GITHUB_BRANCH } = require("./constants.js");
console.log("GITHUB_TOKEN 2", GITHUB_TOKEN);

const octokit = new Octokit({
  auth: GITHUB_TOKEN,
});

console.log("GITHUB_TOKEN 3", GITHUB_TOKEN);

async function writeToGitHub({
  owner,
  repo,
  path,
  githubName,
  email,
  message,
  content,
  phase_name,
}) {
  const branch = GITHUB_BRANCH.hasOwnProperty(phase_name)
    ? GITHUB_BRANCH[phase_name.toLowerCase()]
    : GITHUB_BRANCH.default;
  console.log(
    "GITHUB_NAME",
    GITHUB_NAME,
    githubName,
    GITHUB_BRANCH.hasOwnProperty(phase_name || "default"),
    "x",
    GITHUB_TOKEN,
    "x",
    GITHUB_BRANCH,
    "x",
    phase_name,
    "x",
    branch
  );
  const octokitValues = {
    owner: owner,
    repo: repo,
    path: path,
    message: message,
    content: Base64.encode(content + " " + new Date().toISOString()),
    committer: {
      name: githubName,
      email: email,
    },
    branch,
  };
  const existingCommit = await octokit.repos
    .getContent({
      owner: owner,
      repo: repo,
      path: path,
      ref: branch,
    })
    .catch((error) => {
      console.log("Creating new file");
    });
  if (existingCommit) {
    console.log("Updating existing file", existingCommit);
    octokitValues.sha = existingCommit.data.sha;
    // octokitValues.sha = "fe0cc115c62c0d21439725b4020ad6fe64838d9b";
  }

  console.log("octokitValues", octokitValues);
  const data = await octokit.repos.createOrUpdateFileContents(octokitValues);
  console.log("data", data);
}

module.exports = { writeToGitHub };