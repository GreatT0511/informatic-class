# Google Drive 上のデータを Python で解析する手順

このガイドでは、Google Colab 上で Google ドライブをマウントし、指定したファイルをデータフレームとして読み込んで統計量・ヒストグラム・箱ひげ図を生成する方法を説明します。付属の `drive_analysis.py` を利用すれば、Colab でもローカル環境でも同じ手順で実行できます。

## 1. Google Colab での準備

1. Google Colab を開き、新しいノートブックを作成します。
2. ノートブックの最初のセルでリポジトリをクローンし、必要なライブラリをインストールします。

```python
!git clone https://github.com/GreatT0511/informatic-class.git
%cd informatic-class/google_drive_analysis
!pip install pandas matplotlib
```

## 2. Google ドライブのマウントとデータパスの確認

スクリプトは `--skip-mount` を指定しない限り `google.colab.drive` を使って自動的にドライブをマウントします。Colab のセルで下記のように呼び出してください。

```python
!python drive_analysis.py \
  --data-path "/content/drive/MyDrive/colab-data/sample.csv" \
  --column "score" \
  --output-dir "/content/drive/MyDrive/colab-data/output"
```

- `--data-path` には分析したい CSV / Excel ファイルの絶対パスを設定します。
- `--column` は代表値やヒストグラムを計算したい列名です。
- `--sheet` を付ければ Excel のシートを指定可能です (CSV の場合は不要)。
- `--output-dir` を指定するとヒストグラムや箱ひげ図、統計量のテキストがそのディレクトリに保存されます。

> **補足**: ローカル環境で Drive をマウントする必要がない場合は `--skip-mount` を指定してください。

## 3. スクリプトの構成

`drive_analysis.py` は次の処理を行います。

1. `mount_google_drive`: Colab 上で `drive.mount("/content/drive")` を呼び出し、Drive をマウントします。Colab 以外の環境では自動的にスキップされます。
2. `load_dataframe`: 指定パスから CSV または Excel ファイルを読み込み、pandas の `DataFrame` を生成します。
3. `analyse_dataframe`: 対象列の `describe()` による基本統計量と最頻値を計算し、テキストファイルに書き出します。また、ヒストグラムと箱ひげ図を PNG で保存します。

## 4. 出力されるファイル

- `summary_statistics.txt`: 平均値、標準偏差、中央値などの代表値と最頻値を記録。
- `histogram.png`: 対象列のヒストグラム。
- `boxplot.png`: 対象列の箱ひげ図。

出力ファイルは `--output-dir` で指定したディレクトリに保存されます。Colab では `/content/drive/MyDrive/...` のような Google ドライブ上のパスを指定すると、学習後もファイルが残るので便利です。

## 5. 応用のアイデア

- 複数列を同時に解析したい場合は、`analyse_dataframe` をループで呼び出すか、対象列のリストを引数に取るように拡張します。
- 箱ひげ図やヒストグラムのビン数、色、フォントなどは `matplotlib` のオプションで自由にカスタマイズできます。
- `df.describe(include="all")` を使うとカテゴリカルデータを含む場合でも要約統計を確認できます。

この手順をベースに、Google ドライブ上の任意のデータセットを手軽に可視化・分析できます。
