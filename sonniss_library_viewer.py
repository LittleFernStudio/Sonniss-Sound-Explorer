import os
from textwrap import dedent

path = r"E:\SampleAudioFiles"

counter = 0
FileFullLog = "_wav_file_log.txt"
HTML_file = "index.html"


def extract_folder_name(input_path):
    parts = input_path.split('\\')
    if len(parts) >= 4:
        return parts[3]
    return ""


def extract_file_name(input_path):
    parts = input_path.split('\\')
    if len(parts) >= 5:
        return parts[4]
    return ""


def extract_file_path_rel(input_path):
    parts = input_path.split('\\')
    if len(parts) < 5:
        return ""
    return '/'.join(parts[2:4]) + '/'


def html_escape(value: str) -> str:
    return (
        value.replace("&", "&amp;")
             .replace('"', "&quot;")
             .replace("<", "&lt;")
             .replace(">", "&gt;")
    )


html_code_b = dedent("""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Sonniss Viewer</title>
  <link rel="stylesheet" href="styles.css" />
</head>
<body>
  <div class="wrap">
    <h1>Sonniss GDC Audio Library Viewer</h1>
    <p class="hint">
      You can download the entire GDC library from Sonniss
      <a href="https://sonniss.com/gameaudiogdc/" style="text-decoration: none; font-weight: bold; color: #00ffdd;" target="_blank">here</a>
    </p>

    <div class="toolbar">
      <button id="playAll" type="button">Play All (sequential)</button>
      <button id="pauseAll" type="button">Pause All</button>
      <button id="stopAll" type="button">Stop & Reset</button>
    </div>

    <div class="searchbar-wrap" style="margin: 16px 0;">
      <input
        id="searchInput"
        type="text"
        placeholder="Search by folder name or .wav filename..."
        style="width: 100%; max-width: 500px; padding: 10px 12px; font-size: 16px;"
      />
    </div>

    <section class="grid" id="grid">
""")


def input_variables(row, track_name, audio_src, copy_path, file_name):
    track_name_escaped = html_escape(track_name)
    audio_src_escaped = html_escape(audio_src)
    copy_path_escaped = html_escape(copy_path)
    file_name_escaped = html_escape(file_name)

    # Lowercased searchable text stored as data attributes
    search_folder = html_escape(track_name.lower())
    search_file = html_escape(file_name.lower())

    html_code_m1 = dedent(f"""
      <!-- Item {row} -->
      <figure class="tile"
              data-audio-src="{audio_src_escaped}"
              data-folder-name="{search_folder}"
              data-file-name="{search_file}">
        <figcaption class="title">
          <span class="track">{track_name_escaped}</span>
          <span class="filename">
            <a href="#" class="copy-link" data-filepath="{copy_path_escaped}">{file_name_escaped}</a>
          </span>
        </figcaption>
      </figure>

""")
    return html_code_m1


html_code_e = dedent("""
    </section>
  </div>

  <script>
  document.addEventListener("DOMContentLoaded", () => {
    const tiles = document.querySelectorAll(".tile");
    const searchInput = document.getElementById("searchInput");

    // Create audio player only while hovering the tile
    tiles.forEach(tile => {
      tile.addEventListener("mouseenter", () => {
        // Don't create audio for hidden tiles
        if (tile.style.display === "none") return;

        if (tile.querySelector("audio")) return;

        const src = tile.dataset.audioSrc;
        if (!src) return;

        const audio = document.createElement("audio");
        audio.controls = true;
        audio.preload = "metadata";
        audio.src = src;

        tile.appendChild(audio);
      });

      tile.addEventListener("mouseleave", () => {
        const audio = tile.querySelector("audio");
        if (audio) {
          audio.pause();
          audio.remove();
        }
      });
    });

    // Copy full file path to clipboard when clicking the wav filename
    const copyLinks = document.querySelectorAll(".copy-link");
    copyLinks.forEach(link => {
      link.addEventListener("click", async (e) => {
        e.preventDefault();

        const filePath = link.dataset.filepath;
        if (!filePath) return;

        try {
          await navigator.clipboard.writeText(filePath);

          const originalText = link.textContent;
          link.textContent = "Copied!";
          setTimeout(() => {
            link.textContent = originalText;
          }, 1000);
        } catch (err) {
          console.error("Failed to copy file path:", err);
        }
      });
    });

    // Live search filter by folder name OR wav filename
    if (searchInput) {
      searchInput.addEventListener("input", () => {
        const query = searchInput.value.trim().toLowerCase();

        tiles.forEach(tile => {
          const folderName = tile.dataset.folderName || "";
          const fileName = tile.dataset.fileName || "";

          const matches =
            query === "" ||
            folderName.includes(query) ||
            fileName.includes(query);

          if (!matches) {
            // Remove any active audio if the tile is being hidden
            const audio = tile.querySelector("audio");
            if (audio) {
              audio.pause();
              audio.remove();
            }
          }

          tile.style.display = matches ? "" : "none";
        });
      });
    }

    // Toolbar actions only affect currently visible/hover-created players
    const playAllBtn = document.getElementById("playAll");
    const pauseAllBtn = document.getElementById("pauseAll");
    const stopAllBtn = document.getElementById("stopAll");

    if (playAllBtn) {
      playAllBtn.addEventListener("click", async () => {
        const audios = Array.from(document.querySelectorAll("audio"));
        for (const audio of audios) {
          try {
            audio.currentTime = 0;
            await audio.play();
          } catch (err) {
            console.error("Failed to play audio:", err);
          }
        }
      });
    }

    if (pauseAllBtn) {
      pauseAllBtn.addEventListener("click", () => {
        document.querySelectorAll("audio").forEach(audio => audio.pause());
      });
    }

    if (stopAllBtn) {
      stopAllBtn.addEventListener("click", () => {
        document.querySelectorAll("audio").forEach(audio => {
          audio.pause();
          audio.currentTime = 0;
        });
      });
    }
  });
  </script>
</body>
</html>
""")


with open(FileFullLog, 'w', encoding='utf-8') as FileFullLogHandler, open(HTML_file, 'w', encoding='utf-8') as HTMLFileHandler:
    print("Log files created!")
    HTMLFileHandler.write(html_code_b + "\n")

    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith((".wav", ".Wav", ".WAV")):
                counter += 1
                full_path = os.path.join(root, file)

                # Browser-friendly relative path for the audio src
                audio_src = extract_file_path_rel(full_path) + extract_file_name(full_path)

                # Directory containing the wav file
                copy_path = os.path.dirname(full_path)

                HTMLFileHandler.write(
                    input_variables(
                        str(counter),
                        extract_folder_name(full_path),
                        audio_src,
                        copy_path,
                        extract_file_name(full_path)
                    )
                )

                FileFullLogHandler.write(full_path + "\n")

    HTMLFileHandler.write(html_code_e + "\n")

print(f"Generated {HTML_file} with {counter} .wav files.")