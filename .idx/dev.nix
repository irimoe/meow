{ pkgs, ... }: {
  channel = "stable-24.05"; 

  packages = [
    pkgs.python312Packages.pip
    pkgs.python312
    pkgs.python312Packages.pandas
  ];

  env = {};
  idx = {
    extensions = [
      "ms-python.debugpy"
      "ms-python.python"
      "ms-toolsai.jupyter"
      "ms-toolsai.jupyter-keymap"
      "ms-toolsai.jupyter-renderers" 
      "ms-toolsai.vscode-jupyter-cell-tags"
      "ms-toolsai.vscode-jupyter-slideshow"
    ];

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
