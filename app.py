from flask import Flask, render_template, request, send_file
from pypdf import PdfReader, PdfWriter
import os
import tempfile
import zipfile
import json

app = Flask(__name__)

# ======================================
# TOP
# ======================================

@app.route("/")
def index():
    return render_template("index.html")

# ======================================
# PDF結合
# ======================================

@app.route("/merge")
def merge_page():
    return render_template("merge.html")


@app.route("/merge/run", methods=["POST"])
def merge_run():
    files = request.files.getlist("pdf_files")

    if len(files) < 2:
        return "PDFは2つ以上選択してください"

    output_path = os.path.join(
        tempfile.gettempdir(),
        "merged.pdf"
    )

    merger = PdfWriter()

    for file in files:
        merger.append(file)

    merger.write(output_path)
    merger.close()

    return send_file(
        output_path,
        as_attachment=True,
        download_name="merged.pdf"
    )

# ======================================
# PDF分割
# ======================================

@app.route("/split")
def split_page():
    return render_template("split.html")

@app.route("/split/run", methods=["POST"])
def split_run():

    file = request.files["pdf_file"]

    reader = PdfReader(file)

    total_pages = len(reader.pages)

    if total_pages < 2:
        return "2ページ以上のPDFを指定してください"
        
    temp_dir = tempfile.mkdtemp()

    pdf_files = []

    base_name = os.path.splitext(
    file.filename
    )[0]

    for page_num in range(total_pages):

        writer = PdfWriter()
        writer.add_page(
            reader.pages[page_num]
        )

        output_pdf = os.path.join(
            temp_dir,
            f"{base_name}_{page_num + 1}.pdf"
        )

        with open(output_pdf, "wb") as output:
            writer.write(output)

        pdf_files.append(output_pdf)

    zip_path = os.path.join(
        temp_dir,
        "split_result.zip"
    )

    with zipfile.ZipFile(
    zip_path,
    "w",
    zipfile.ZIP_DEFLATED
    ) as zipf:

        for pdf_file in pdf_files:

            zipf.write(
            pdf_file,
            arcname=os.path.basename(pdf_file)
        )

    return send_file(
        zip_path,
        as_attachment=True,
        download_name="split_result.zip"
)

# ======================================
# PDF削除
# ======================================

@app.route("/delete")
def delete_page():
    return render_template("delete.html")

@app.route("/delete/run", methods=["POST"])
def delete_run():

    file = request.files["pdf_file"]

    try:
        delete_page_num = int(
        request.form["page_number"]
    )

    except ValueError:
        return "ページ番号は数字で入力してください"

    reader = PdfReader(file)

    total_pages = len(reader.pages)

    if total_pages < 2:
        return "2ページ以上のPDFを指定してください"

    if (
    delete_page_num < 1
    or delete_page_num > total_pages
    ):
        return "存在しないページです"

    writer = PdfWriter()

    for i, page in enumerate(
    reader.pages,
    start=1
    ):

        if i != delete_page_num:
            writer.add_page(page)

    base_name = os.path.splitext(
    file.filename
    )[0]

    output_path = os.path.join(
    tempfile.gettempdir(),
    f"{base_name}_deleted.pdf"
)

    with open(output_path, "wb") as output:
        writer.write(output)

    return send_file(
    output_path,
    as_attachment=True,
    download_name=f"{base_name}_deleted.pdf"
)

# ======================================
# PDF並び替え・回転
# ======================================

@app.route("/reorder")
def reorder_page():
    return render_template("reorder.html")


@app.route("/reorder/run", methods=["POST"])
def reorder_run():

    file = request.files.get("pdf_file")

    if not file:
        return "PDFファイルを選択してください", 400

    order_json = request.form.get("page_order")

    if not order_json:
        return "ページ順序の情報がありません", 400

    try:
        page_order = json.loads(order_json)
    except (TypeError, ValueError):
        return "ページ順序の情報が不正です", 400

    if not isinstance(page_order, list) or len(page_order) == 0:
        return "ページ順序の情報が不正です", 400

    reader = PdfReader(file)
    total_pages = len(reader.pages)

    writer = PdfWriter()

    for item in page_order:

        try:
            index = int(item["index"])
            rotation = int(item.get("rotation", 0)) % 360
        except (KeyError, TypeError, ValueError):
            return "ページ順序の情報が不正です", 400

        if index < 0 or index >= total_pages:
            return "存在しないページが指定されました", 400

        page = reader.pages[index]

        if rotation:
            page.rotate(rotation)

        writer.add_page(page)

    base_name = os.path.splitext(
        file.filename
    )[0]

    output_path = os.path.join(
        tempfile.gettempdir(),
        f"{base_name}_reordered.pdf"
    )

    with open(output_path, "wb") as output:
        writer.write(output)

    return send_file(
        output_path,
        as_attachment=True,
        download_name=f"{base_name}_reordered.pdf"
    )


# ======================================
# 起動
# ======================================

if __name__ == "__main__":
    app.run(debug=True)
