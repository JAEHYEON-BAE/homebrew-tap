cask "bloct" do
  version "1.7.5"
  sha256 "9e822849709ce3fa53924c68a3ae76eb007b6c361750c0ef28dd0955f4ba741e"

  url "https://github.com/JAEHYEON-BAE/bloct/releases/download/v#{version}/Bloct.zip"
  name "Bloct"
  desc "Native macOS markdown viewer and editor"
  homepage "https://github.com/JAEHYEON-BAE/bloct"

  app "Bloct.app"
end
