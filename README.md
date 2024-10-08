# aminome

**A**dd all **mi**sskey **no**tes to **Me**ilisearch.

## これは何

- Misskeyサーバーの全ノートをMeilisearchへ登録するPythonスクリプトです。
- [Meilisearchで導入以前の過去のノートを検索できるようにマイグレーションしたい](https://github.com/misskey-dev/misskey/issues/10789) を実現します。
- ID採番方式がaidまたはaidxのMisskeyサーバーに対応しています。

## 使い方

1. python packageをインストールします。

    ```sh
    python3 -m venv .aminome
    source .aminome/bin/activate
    pip3 install -r requirements.txt
    ```

2. 設定ファイルをコピーし、編集します。

    ```sh
    cp config/example.yml config/config.yml
    ```

    設定ファイルはMisskeyの `default.yml` を参考にすると良いでしょう。  
    - Meilisearchの `apiKey` はMeilisearchのAPIキーを指定します。
    - Meilisearchの `index` はデフォルトではMisskeyのドメイン(ドットをハイフンに置き換えた文字列)になります。

    ```yaml
    db:
        host: localhost
        port: 5432
        db: misskey
        user: example-misskey-user
        pass: example-misskey-pass

    meilisearch:
        host: localhost
        port: 7700
        apiKey: 'your-api-key'
        index: 'example-com'
        scope: local
        ssl: false
    ```

3. aminomeを実行します。

    ```sh
    python3 ./aminome.py
    ```

## 参考実装

以下のスクリプトを参考にしました。ありがとうございます。

- [dump_misskey_note_data.py](https://gist.github.com/CyberRex0/d481c4c2be6dc47fee4b50cefadf2074)
- [mattyatea/misskey-meilisearch-oldnote-index](https://github.com/mattyatea/misskey-meilisearch-oldnote-index)
