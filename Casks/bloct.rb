cask "bloct" do
  version "1.6.3"
  sha256 "95ea8121e8e6a8ac4dc2bf00b1841c1274177e75ef0b96eaf5121ddf2047abc0"

  url "https://github.com/JAEHYEON-BAE/bloct/releases/download/v#{version}/Bloct.zip"
  name "Bloct"
  desc "Native macOS markdown viewer and editor"
  homepage "https://github.com/JAEHYEON-BAE/bloct"

  app "Bloct.app"
end
