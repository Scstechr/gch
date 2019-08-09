
class Gch < Formula
  desc "Git Commit Handler: A tool to handle git related commands easier."
	homepage "https://github.com/Scstechr/gch"
  url "https://github.com/Scstechr/gch/releases/download/v1.13/gch_v1.13.tar.gz"
  sha256 "74525cadfb6c1e8b76e01b1ca8cf0cbd62f3d1fb216937a265fb0e6fca04d38b"

  def install
		bin.install "gch"
		bin.install "gdiff"
  end

end
    
['', 'class Gch < Formula', '  desc Git Commit Handler: A tool to handle git related commands easier.', '	homepage https://github.com/Scstechr/gch', '  url https://github.com/Scstechr/gch/releases/download/v1.13/gch-v1.13.tar.gz', '  sha256 f03154ed0b971559684a4be7874cfd85ec77db620a2ed0525238ac3c032b241a', '', '  def install', '		bin.install gch', '		bin.install gdiff', '  end', '', 'end', '    ']
