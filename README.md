# TLDR Discord Bot

매일 아침 [TLDR Tech](https://tldr.tech) 뉴스레터를 Discord에 자동으로 전송하는 GitHub Actions 봇입니다.

**완전 무료** — GitHub Actions + Discord Webhook만 사용합니다.

---

## 설정 방법 (5분이면 끝)

### 1단계: Discord Webhook URL 만들기

1. Discord 서버에서 뉴스를 받고 싶은 **채널**로 이동
2. 채널 이름 우클릭 → **채널 편집** → **연동** → **웹후크** → **새 웹후크**
3. 이름 설정 후 **웹후크 URL 복사** → 어딘가에 저장해 두기

### 2단계: GitHub 레포 만들기

1. [github.com](https://github.com) 에서 **New repository** (Public or Private 모두 무료 동작)
2. 이 폴더 전체를 레포에 업로드하거나 `git push`

```bash
cd tldr-discord-bot
git init
git add .
git commit -m "init: TLDR Discord bot"
git remote add origin https://github.com/<your-username>/<repo-name>.git
git push -u origin main
```

### 3단계: GitHub Secret 등록

1. GitHub 레포 페이지 → **Settings** → **Secrets and variables** → **Actions**
2. **New repository secret** 클릭
3. Name: `DISCORD_WEBHOOK_URL`
4. Secret: 1단계에서 복사한 Webhook URL 붙여넣기
5. **Add secret** 클릭

### 4단계: 테스트 실행

1. GitHub 레포 → **Actions** 탭
2. **TLDR Daily Discord Bot** 워크플로우 선택
3. **Run workflow** → **Run workflow** 클릭
4. Discord 채널에 메시지가 오면 성공!

---

## 실행 스케줄

기본값: **평일 오전 9시 (KST)** 자동 전송

변경하려면 `.github/workflows/daily_tldr.yml`의 cron 값을 수정:

```yaml
# 매일 오전 8시 (KST)로 변경하고 싶다면:
- cron: "0 23 * * *"   # UTC 23:00 = KST 08:00

# 주말 포함 매일 받고 싶다면:
- cron: "0 0 * * *"
```

> [crontab.guru](https://crontab.guru) 에서 cron 표현식을 시각적으로 확인할 수 있습니다.

---

## 수신하는 뉴스레터

| 뉴스레터 | RSS 피드 |
|---|---|
| 💻 TLDR Tech | `https://tldr.tech/tech/rss` |
| 🤖 TLDR AI | `https://tldr.tech/ai/rss` |

다른 TLDR 채널을 추가하고 싶다면 `fetch_tldr.py`의 `FEEDS` 리스트에 항목을 추가하세요.

<details>
<summary>사용 가능한 TLDR RSS 피드 목록</summary>

- `https://tldr.tech/tech/rss` — Tech
- `https://tldr.tech/ai/rss` — AI
- `https://tldr.tech/webdev/rss` — Web Dev
- `https://tldr.tech/devops/rss` — DevOps
- `https://tldr.tech/infosec/rss` — InfoSec
- `https://tldr.tech/product/rss` — Product
- `https://tldr.tech/design/rss` — Design
- `https://tldr.tech/marketing/rss` — Marketing
- `https://tldr.tech/crypto/rss` — Crypto
- `https://tldr.tech/founders/rss` — Founders

</details>
