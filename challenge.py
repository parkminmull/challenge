import requests  # requestsライブラリをインポートする
import time      # timeライブラリをインポートする

def start_challenge(nickname):
    # チャレンジを開始するためにサーバーにPOSTリクエストを送る関数
    url = "http://challenge.z2o.cloud/challenges"  # APIエンドポイントのURL
    params = {'nickname': nickname}  # ニックネームをパラメータとして設定
    response = requests.post(url, params=params)  # POSTリクエストを送信してレスポンスを受け取る
    print("POSTレスポンスステータス:", response.status_code)  # ステータスコードを表示
    if response.status_code == 201:
        print("チャレンジが正常に開始されました。:", response.json())  # チャレンジ開始成功時のレスポンスを表示
        return response.json()  # JSONデータを返す
    else:
        print("チャレンジの開始に失敗しました。:", response.json())  # 失敗時のレスポンスを表示
        return None  # Noneを返す

def send_request(challenge_id, actives_at):
    # 指定された時間にAPIエンドポイントにPUTリクエストを送る関数
    url = f"http://challenge.z2o.cloud/challenges"  # APIエンドポイントのURL
    headers = {'X-Challenge-Id': challenge_id}  # ヘッダーにチャレンジIDを設定
    while True:
        current_time = time.time() * 1000  # 現在時刻をミリ秒単位で取得
        if current_time >= actives_at - 100:  # 指定時間の直前にリクエストを送信
            response = requests.put(url, headers=headers)  # PUTリクエストを送信してレスポンスを受け取る
            print("PUTレスポンス:", response.json())  # レスポンス内容を表示
            return response.json()  # JSONデータを返す

def run_challenge():
    nickname = input("ニックネームを入力してください: ")  # ユーザーにニックネームの入力を促す
    challenge_data = start_challenge(nickname)  # チャレンジを開始する関数を呼び出し
    if challenge_data:
        challenge_id = challenge_data['id']  # チャレンジIDを取得
        actives_at = challenge_data['actives_at']  # 活動開始時刻を取得
        total_diff = 0  # 時間差の合計を初期化

        while total_diff < 500:  # 合計時間差が500未満の間繰り返す
            response = send_request(challenge_id, actives_at)  # 指定時間にリクエストを送る
            called_at = time.time() * 1000  # リクエスト送信時刻をミリ秒単位で記録
            print("リクエスト送信時刻:", called_at)  # 送信時刻を表示
            server_called_at = response.get('called_at', called_at)  # サーバーからの応答時刻を取得
            print("サーバー応答時刻:", server_called_at)  # 応答時刻を表示
            time_diff = max(0, called_at - server_called_at)  # 時間差を計算
            print("このリクエストの時間差:", time_diff)  # 時間差を表示
            total_diff += time_diff  # 合計時間差に加算
            print("合計時間差:", total_diff)  # 合計時間差を表示
            if 'result' in response:
                print("チャレンジ結果:", response['result'])  # チャレンジの結果を表示
                break  # チャレンジ終了
            actives_at = response['actives_at']  # 次の活動可能時刻を更新
            print("次の活動可能時刻:", actives_at)  # 次の活動可能時刻を表示
    else:
        print("チャレンジデータの取得に失敗しました。")  # データ取得失敗を表示

if __name__ == "__main__":
    run_challenge()  # メイン関数を実行
