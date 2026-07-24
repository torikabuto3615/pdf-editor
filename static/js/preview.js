// ドロップゾーンの見た目を、選択されたファイルに応じて更新する
function updateDropzoneLabel(zone, files) {
    const label = zone.querySelector(".dropzone-label");
    if (!label) return;

    if (!files || files.length === 0) {
        label.textContent = zone.dataset.defaultLabel || "クリックまたはドラッグしてPDFを選択";
        zone.classList.remove("has-file");
        return;
    }

    zone.classList.add("has-file");

    if (files.length === 1) {
        label.textContent = files[0].name;
    } else {
        label.textContent = `${files.length}件のファイルを選択済み`;
    }
}

// ドラッグ&ドロップでのファイル選択を有効にする
// zoneId: <label class="dropzone"> のid
// inputId: 対になる <input type="file"> のid
function setupDropzone(zoneId, inputId) {
    const zone = document.getElementById(zoneId);
    const input = document.getElementById(inputId);

    if (!zone || !input) {
        return;
    }

    input.addEventListener("change", () => {
        updateDropzoneLabel(zone, input.files);
    });

    ["dragenter", "dragover"].forEach((evt) => {
        zone.addEventListener(evt, (e) => {
            e.preventDefault();
            zone.classList.add("is-dragover");
        });
    });

    ["dragleave", "drop"].forEach((evt) => {
        zone.addEventListener(evt, (e) => {
            e.preventDefault();
            zone.classList.remove("is-dragover");
        });
    });

    zone.addEventListener("drop", (e) => {
        const dt = e.dataTransfer;
        if (dt && dt.files && dt.files.length > 0) {
            input.files = dt.files;
            input.dispatchEvent(new Event("change"));
        }
    });
}

// PDF.js のワーカー設定(CDNから読み込み)
pdfjsLib.GlobalWorkerOptions.workerSrc =
    "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js";

// PDFファイルのページ数を取得する
async function getPdfPageCount(file) {
    const buffer = await file.arrayBuffer();
    const pdf = await pdfjsLib.getDocument({ data: buffer }).promise;
    return pdf.numPages;
}

// ファイル選択時に「ファイル名(ページ数)」を表示するプレビューを設定する
// inputId: <input type="file"> のid
// infoId : プレビューを表示する要素のid
function setupPdfPreview(inputId, infoId) {
    const input = document.getElementById(inputId);
    const info = document.getElementById(infoId);

    if (!input || !info) {
        return;
    }

    input.addEventListener("change", async () => {
        const files = Array.from(input.files);

        if (files.length === 0) {
            info.style.display = "none";
            info.innerHTML = "";
            return;
        }

        info.style.display = "block";
        info.innerHTML = "読み込み中...";

        try {
            const lines = [];

            for (const file of files) {
                const pageCount = await getPdfPageCount(file);
                lines.push(
                    `📄 ${file.name}<span class="page-count">（${pageCount}ページ）</span>`
                );
            }

            info.innerHTML = lines.join("<br>");
        } catch (err) {
            info.innerHTML = "⚠️ PDFの情報を読み取れませんでした（壊れたファイルの可能性があります）";
        }
    });
}
