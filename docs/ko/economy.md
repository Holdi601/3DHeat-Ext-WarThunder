---
title: 경제
nav_order: 14
lang: ko
source: economy.md
source_hash: "870b7f982c6d"
nav_exclude: true
search_exclude: true
---
# 경제 {#economy}

전투에 얼마가 들었고 얼마를 벌었는지를 나타내는 열이에요. 이 값들은 변환할 때 **여러분의 설치본**에서 읽어요(`char.vromfs.bin`: 차량별 `config/wpcost.blk`, `config/warpoints.blk`와 `config/rank.blk`. `aces.vromfs.bin`의 무기 blk는 각 탄이 어떤 개조인지 알려 줘요). 게임의 숫자는 이 저장소에 하나도 없어요. 값은 여러분 자신의 출력에만 들어가요. 설치본의 `char.vromfs.bin`이 없으면 경제 데이터는 전혀 쓰이지 않아요(`economy.available`이 false). 가격은 전투 난이도에 맞는 것을 써요(RB는 `repairCostHistorical`, AB는 `...Arcade`, SB는 `...Simulation`).

| 열 | 행 | 내용 |
|---|---|---|
| `cost_fired_sl` | `bullet_rearm`(발사 후 다시 장전한 탄, 지상 차량), `launch`(항공기, 헬리콥터) | 발사한 탄, 로켓, 미사일, 폭탄의 SL 비용 |
| `cost_lost_sl` | 플레이어 차량의 `death` | 차량의 수리 비용(기본형; 블록에 있는 완전 업그레이드형) |
| `earn_sl`, `earn_rp` | `reward`(새 이벤트, 획득한 사람의 위치와 시각에) | 번 SL과 RP |
| `rewardType` | `reward` | `kill`, `assist`, `capture`, `base_damage`, `damage`, `missile_evade`, `critical_hit`, `severe_damage`, `scouting`, `other`, `battle_end` |
| `currency` | `cost_*` 또는 `earn_sl`이 있는 모든 행 | `SL` (`earn_rp`는 연구 포인트) |
| `econ_basis` | 같은 행들 | `install`(설치본에서 읽은 가격) 또는 `inferred`(아래처럼 계산한 값) |

**누가 이겼나.** 리플레이가 알려 주는 경우, 팀의 모든 행에 `won`(0/1)이 들어가요. 클라이언트 리플레이의 결과에는 녹화자 자신의 결과(`status`: `success` 또는 `fail`)가 있어서, 녹화자의 팀이 이겼는지 졌는지, 그리고 상대 팀은 반대인지 알 수 있어요. 매치 문서의 `result`가 이것을 말해 줘요(`winner`, `status`, `authorTeam`). 서버 리플레이와 끝나기 전에 떠난 리플레이에는 결과가 없어요(서버 리플레이의 `status`는 항상 `success`이고 녹화자를 가리키지 않아요). 이런 리플레이에는 설치된 개조 정보도 없어요. 결과에는 각 플레이어의 차량이 이름과 종류로만 나와요. 그래서 `won`은 비어 있어요.

뷰어의 비용 모델은 `currency`가 붙은 `cost_*`(와 `earn_*`) 열을 읽어요. `cost_fired_sl + cost_lost_sl`을 합하면 실버 라이온을 어디에 쓰고 잃었는지 나오고, `earn_sl`은 어디서 벌었는지 나와요. 처치의 보상은 `kill` 행이 아니라 `reward` 행에 있어서 아무것도 두 번 세지 않아요.

- **발사한 탄**(`install`: 슬롯의 탄을 알 때 - 처치가 이름을 알려 줬어요, [명중 결과](hits.md#hit-outcomes) 참고 - 아니면 `inferred`: 그 차량에서 그 포가 쏠 수 있는 탄들의 평균 가격. 기본 탄은 무료예요. 기관총은 리플레이가 세지 않으므로 비용이 없어요).
- **발사기**(`inferred`): 게임은 항공기의 무장 프리셋을 항목 하나가 아니라 출격 단위로 가격을 매겨요. 항목 하나의 값은 차량의 가격이 붙은 프리셋들의 (가격 / 항목 수) 중앙값이에요(`sum_weapons`; 대응책과 보조 연료탱크는 뺌). 가격이 없는 프리셋만 있으면 0이에요.
- **보상**(모두 `inferred`): 리플레이에는 보상 기록이 없어요. 결과 블록에는 점수와 개수만 있고, 실버 라이온을 실어 나르는 메시지는 없어요(클라이언트와 서버 리플레이 모두에서 확인했어요). `kill`은 `aKill` × 처치한 사람의 `rewardMul<mode>` × 피해자 클래스의 가중치(warpoints.blk의 `units`, 그 `unitClass`로) × AI 피해자라면 `aiKillK` × 항공기가 지상 유닛을 처치하면 `groundKillMul`을 받아요. RP도 같은데 `expMul`과 rank.blk의 가중치를 써요. 복제된 점수판에서 그 밖의 점수 변화는 모두, 그 점수만큼의 가치를 그 전투의 점당 SL로 환산한 보상이에요(처치의 SL을 처치 단계의 점수 중앙값으로 나눈 값; 블록의 `pointsPerKill`). 종류는 함께 오른 카운터(어시스트, 점령 구역, 구역 피해, 피해 보상, 미사일 회피)로 정해요. 없으면 3초 안의 그 플레이어의 치명타 또는 중대 피해, 없으면 플레이어 유닛의 탐지(2초 안, `scouting`), 그 밖에는 `other`예요. `battle_end`는 플레이어의 전투 중 수입에 대한 `winK`(승리) 또는 `defeatK`(패배)예요. 승자는 팀의 남은 티켓으로 가리고, 같으면 점수로 가려요. 프리미엄 시간, 부스터, 승무원, 개조는 알 수 없어서 적용하지 않아요. 지상 전투의 처치 예산(`def_ground_kill_wp_budget*`)은 모델링하지 않아요.

매치 문서의 `economy`(그리고 `.3dheat` 컨테이너에서는 매니페스트의 `extensions["heat3d/economy"]`)는 `currency` `SL`, `researchCurrency` `RP`, `difficulty`, `totals`(`firedSl`, `lostSl`, `earnedSl`, `earnedRp`), `players`(플레이어별로 같은 값, `netSl` 포함), `vehicles`(플레이어 차량별: `repairSl`, `repairFullUpgradedSl`, `purchaseSl`, `researchRp`, `crewSl`, `crewExpertSl`, `rewardMul`, `expMul`, `groundKillMul`, `battleTimeAwardSl`, `rank`, `economicRank`, `unitClass`), `multipliers`(`aKill`, `aiKillK`, `winK`, `defeatK`, `wpMultiplier`), `winnerTeam`, `pointsPerKill`, `check`(종류별로 몇 행이 가격이 매겨졌는지, 추정됐는지, 가격이 없었는지)를 담아요.

---

[3DHeat](https://github.com/Holdi601/3DHeat)의 일부([문서](https://holdi601.github.io/3DHeat/)). 소스: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
