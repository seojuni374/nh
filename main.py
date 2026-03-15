#!/usr/bin/env python3
# main.py — 진입점
# 사용법:
#   python main.py              → 전체 파이프라인 실행 + PDF 생성
#   python main.py --query 삼성전자
#   python main.py --query NVDA
#   python main.py --query 반도체
#   python main.py --no-report  → 리포트 없이 분석만

import sys
import os
import argparse

# 프로젝트 루트를 경로에 추가
sys.path.insert(0, os.path.dirname(__file__))

from orchestrator import ChiefOrchestrator


def main():
    parser = argparse.ArgumentParser(
        description="퀀트 트레이딩 시스템 — 코스피·나스닥 반도체·AI·전력·원자력·우주"
    )
    parser.add_argument("--query", "-q", type=str, help="종목 또는 섹터 조회 (예: 삼성전자, NVDA, 반도체)")
    parser.add_argument("--no-report", action="store_true", help="PDF 보고서 생성 스킵")
    parser.add_argument("--interactive", "-i", action="store_true", help="대화형 모드")
    parser.add_argument("--learn", action="store_true", help="자기학습 루프 실행 (전일 예측 평가 + 팀 토의)")
    parser.add_argument("--status", action="store_true", help="학습 현황 및 파라미터 버전 출력")
    args = parser.parse_args()

    orch = ChiefOrchestrator()

    if args.status:
        orch.show_learning_status()
        return

    if args.learn:
        orch.run_learning_loop()
        return

    if args.query:
        # 쿼리 모드: 전체 파이프라인 + 특정 종목 상세
        print("\n🎼 Chief Orchestrator — 분석 시작...")
        orch.run_full_pipeline(generate_report=not args.no_report)
        print(orch.query_ticker(args.query))

    elif args.interactive:
        # 대화형 모드
        print("\n🎼 퀀트 트레이딩 시스템 — 대화형 모드")
        print("명령어: 종목명/티커 입력, 'run' 으로 전체 실행, 'report' 로 PDF 생성, 'quit' 종료\n")

        orch.run_full_pipeline(generate_report=False)
        orch.print_summary()

        while True:
            try:
                user_input = input("\n종목 조회 > ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n종료합니다.")
                break

            if not user_input:
                continue
            if user_input.lower() in ("quit", "exit", "종료"):
                break
            elif user_input.lower() == "run":
                orch.run_full_pipeline(generate_report=False)
                orch.print_summary()
            elif user_input.lower() == "report":
                from report.daily_report import generate_pdf
                path = generate_pdf(orch.last_results)
                print(f"✓ PDF 저장: {path}")
            elif user_input.lower() in ("learn", "학습"):
                orch.run_learning_loop()
            elif user_input.lower() in ("status", "현황"):
                orch.show_learning_status()
            else:
                print(orch.query_ticker(user_input))

    else:
        # 기본: 전체 파이프라인 + PDF
        report_path = orch.run_full_pipeline(generate_report=not args.no_report)
        orch.print_summary()
        if report_path:
            print(f"\n📄 PDF 보고서: {report_path}")


if __name__ == "__main__":
    main()
