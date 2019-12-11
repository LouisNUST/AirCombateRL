#!usr/bin/env python3
# -*- coding: utf-8 -*-

import torch
import sys
sys.path.append('..')
import envs
from models.dqn import DQN
#from argument.dqnArgs import args
import common.alloc as alloc
from common.utlis import set_seed
from interactor.episodeSelfPlay import run_AirCombat_selfPlay
from argument.argManage import args
from sacred import Experiment
from sacred.observers import FileStorageObserver
from common.config import args_wrapper_checkpoint_folder
from common.config import add_ex_config_obs

ex = Experiment('selfPlay1A1U')

@ex.main
def my_main():
    set_seed(args.seed)
    # print(ex.current_run._id)
    if args.flag_is_train:
        args_wrapper_checkpoint_folder(args, ex.current_run._id)
    print(args.save_path)
    run()

def run():
    env = envs.make(args.env_name)

    flag_is_train = args.flag_is_train    # flag_is_train = 1, 一个训练，一个使用； flag_is_train = 0, 两个都是在使用（根据train_agent状态决定输出谁的信息---flag_train_blue）
    flag_focus_blue = args.flag_focus_blue    # flag_focus_blue = 1 时训练agent_blue； flag_train_blue = 0 时训练agent_red

    if flag_focus_blue:
        train_agent_name = 'blue'
        red_agent  = DQN(env.state_dim, env.action_dim, is_train=False, scope='red')
        blue_agent = DQN(env.state_dim, env.action_dim, is_train=flag_is_train, scope='blue')
        alloc.check_scheme(blue_agent.is_train, red_agent.is_train, train_agent_name)
        run_AirCombat_selfPlay(env, blue_agent, red_agent, train_agent_name)
    else:
        train_agent_name = 'red'
        blue_agent = DQN(env.state_dim, env.action_dim, is_train=False, scope='blue')
        red_agent  = DQN(env.state_dim, env.action_dim, is_train=flag_is_train, scope='red')
        alloc.check_scheme(blue_agent.is_train, red_agent.is_train, train_agent_name)
        run_AirCombat_selfPlay(env, red_agent, blue_agent, train_agent_name)

if __name__ == "__main__":
    '''
    参数传递；
    参数打印；
    高阶逻辑；
    等...
    '''
    # 添加观察者和配置文件
    add_ex_config_obs(ex, args, result_path=None)
    set_seed(args.seed)
    ex.run_commandline()
    # run()