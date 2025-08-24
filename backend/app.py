import sys
import argparse
import threading
import time
import schedule
from datetime import datetime

# 导入日志配置
from config.logging_config import get_logger
from router import app
from app.main import job
from config.settings import SCHEDULE_TIME

# 创建日志记录器
logger = get_logger('app', 'INFO')

def run_web_server(host='127.0.0.1', port=5001, debug=True):
    """
    启动Web API服务器
    """
    logger.info(f"🌐 Starting Web API server on http://{host}:{port}")
    app.run(host=host, port=port, debug=debug, use_reloader=False)

def run_scheduler():
    """
    运行定时任务调度器
    """
    logger.info(f"🕒 Scheduled job to run every day at {SCHEDULE_TIME}")
    logger.info("🏃 Performing initial run immediately...")
    
    # 立即执行一次任务
    try:
        job()
    except Exception as e:
        logger.error(f"❌ Initial job execution failed: {e}")
    
    # 设置定时任务
    schedule.every().day.at(SCHEDULE_TIME).do(job)
    
    logger.info("⏰ Scheduler started, waiting for scheduled tasks...")
    while True:
        try:
            schedule.run_pending()
            time.sleep(60)  # 每分钟检查一次
        except KeyboardInterrupt:
            logger.info("🛑 Scheduler interrupted by user")
            break
        except Exception as e:
            logger.error(f"❌ Scheduler error: {e}")
            time.sleep(60)

def run_reporter_only():
    """
    仅运行报告生成器（不启动Web服务）
    """
    logger.info("📊 Running GitHub Trending Reporter (Reporter Only Mode)")
    run_scheduler()

def run_web_only(host='127.0.0.1', port=5001, debug=True):
    """
    仅运行Web API服务（不运行定时任务）
    """
    logger.info("🌐 Running GitHub Trending Reporter (Web Only Mode)")
    run_web_server(host, port, debug)

def run_full_service(host='127.0.0.1', port=5001, debug=False):
    """
    运行完整服务（Web API + 定时任务）
    """
    logger.info("🚀 Starting GitHub Trending Reporter (Full Service Mode)")
    logger.info("=" * 60)
    
    # 在单独的线程中运行定时任务
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    
    # 在主线程中运行Web服务器
    try:
        run_web_server(host, port, debug)
    except KeyboardInterrupt:
        logger.info("🛑 Service interrupted by user")
    except Exception as e:
        logger.error(f"❌ Service error: {e}")
    finally:
        logger.info("🔚 Service shutdown complete")

def main():
    """
    主函数 - 解析命令行参数并启动相应服务
    """
    parser = argparse.ArgumentParser(
        description='GitHub Trending Reporter - 统一启动入口',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
运行模式说明:
  full      运行完整服务 (Web API + 定时任务) [默认]
  web       仅运行Web API服务
  reporter  仅运行定时报告生成器

示例:
  python app.py                              # 运行完整服务
  python app.py --mode web --port 8080      # 仅运行Web服务，端口8080
  python app.py --mode reporter             # 仅运行定时任务
  python app.py --host 0.0.0.0 --debug     # 运行完整服务，监听所有地址，开启调试
        """
    )
    
    parser.add_argument(
        '--mode', 
        choices=['full', 'web', 'reporter'], 
        default='full',
        help='运行模式 (默认: full)'
    )
    
    parser.add_argument(
        '--host', 
        default='127.0.0.1',
        help='Web服务监听地址 (默认: 127.0.0.1)'
    )
    
    parser.add_argument(
        '--port', 
        type=int, 
        default=5001,
        help='Web服务端口 (默认: 5001)'
    )
    
    parser.add_argument(
        '--debug', 
        action='store_true',
        help='启用调试模式 (仅在web/full模式下生效)'
    )
    
    args = parser.parse_args()
    
    logger.info("🚀 GitHub Trending Reporter")
    logger.info("=" * 60)
    logger.info(f"📅 Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"🎯 Mode: {args.mode}")
    if args.mode in ['web', 'full']:
        logger.info(f"🌐 Web service: http://{args.host}:{args.port}")
        logger.info(f"🐛 Debug mode: {'ON' if args.debug else 'OFF'}")
    if args.mode in ['reporter', 'full']:
        logger.info(f"⏰ Scheduled time: {SCHEDULE_TIME}")
    logger.info("=" * 60)
    
    # 根据模式启动相应服务
    try:
        if args.mode == 'full':
            run_full_service(args.host, args.port, args.debug)
        elif args.mode == 'web':
            run_web_only(args.host, args.port, args.debug)
        elif args.mode == 'reporter':
            run_reporter_only()
    except KeyboardInterrupt:
        logger.info("🛑 Application interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Application error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()