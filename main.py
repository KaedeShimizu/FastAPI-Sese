# 这里是主程序
# 因为现在有多个版本的程序，所以在这里进行一下分流
# 目前推荐使用jitsu版本
import main_jitsu
import uvicorn

uvicorn.run(main_jitsu.app, host="127.0.0.1", port=8000)