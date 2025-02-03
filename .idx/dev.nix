{ pkgs, ... }: {
  channel = "stable-24.05";

  # Use https://search.nixos.org/packages to find packages
  packages = [
    pkgs.python312Packages.pandas
    pkgs.python312Packages.pip
    pkgs.python312
  ];

  env = {};
  idx = {
    extensions = [  "ms-toolsai.jupyter" "ms-toolsai.jupyter-keymap" "ms-toolsai.jupyter-renderers" "ms-toolsai.vscode-jupyter-cell-tags" "ms-toolsai.vscode-jupyter-slideshow"];

    previews = {
      enable = true;
      previews = { };
    };

    workspace = {
      onCreate = { };
      onStart = { };
    };
  };
}
