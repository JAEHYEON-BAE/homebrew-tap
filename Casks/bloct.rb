cask "bloct" do
  version "1.7.0"
  sha256 "2e39575d73685469cee6577d05d2947fe959e72708bf81dea6e85dc874834142"

  url "https://github.com/JAEHYEON-BAE/bloct/releases/download/v#{version}/Bloct.zip"
  name "Bloct"
  desc "Native macOS markdown viewer and editor"
  homepage "https://github.com/JAEHYEON-BAE/bloct"

  app "Bloct.app"
end
