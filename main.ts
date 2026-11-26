// Entry point: regenerate entry.png (1024x1024) by running draw_image.py,
// which lives next to this file. No embedded image data.
import { execFileSync } from "node:child_process";
import { dirname } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
execFileSync("python3", [`${here}/draw_image.py`], { stdio: "inherit" });
console.log("entry.png written");
