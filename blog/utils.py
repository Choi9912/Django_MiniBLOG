import requests  # type: ignore


def suggest_title_improvement(original_title):
    api_url = "https://open-api.jejucodingcamp.workers.dev/"
    prompt = (
        f"다음 블로그 제목을 더 흥미롭고 매력적으로 개선해주세요: '{original_title}'"
    )

    data = {
        "prompt": prompt,
        "max_tokens": 50,
    }

    try:
        response = requests.post(api_url, json=data)
        response.raise_for_status()  # 에러 발생 시 예외를 발생시킵니다.
        improved_title = response.json()["choices"][0]["text"].strip()
        return improved_title
    except requests.RequestException as e:
        print(f"API 호출 중 오류 발생: {e}")
        return original_title
