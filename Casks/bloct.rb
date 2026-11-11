cask "bloct" do
  version "2.0.1"
  sha256 "09e49fc197b98ee20124bc9b19efd057adc1b057af9d511b83f899e5f7f36a10"

  url "https://github.com/JAEHYEON-BAE/bloct/releases/download/v#{version}/Bloct.zip"
  name "Bloct"
  desc "Native macOS markdown viewer and editor"
  homepage "https://github.com/JAEHYEON-BAE/bloct"

  app "Bloct.app"
end
