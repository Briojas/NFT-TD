import { useWeb3React, Web3ReactHooks, Web3ReactProvider } from '@web3-react/core';
import type { MetaMask } from '@web3-react/metamask';

import { hooks as metaMaskHooks, metaMask } from './connectors/metamask';
import { getName } from './utils';
import { NavBar } from './components/nav-bar/nav-bar';
import { TowerCard, TowerData } from './components/tower-card/tower-card';
import { Icon } from '@blueprintjs/core';
import App_module from './App.module.scss';
import { useEffect } from 'react';
import { Value } from 'classnames';

const connectors: [MetaMask, Web3ReactHooks][] = [[metaMask, metaMaskHooks]];

function Submit(data: TowerData) {
    const { connector } = useWeb3React();
    const { isActive, chainId, account, provider } = useWeb3React();
    // console.log(`Priority Connector is: ${getName(connector)}`);
    // console.log(isActive, chainId, account, provider);

    function joinQueue(data: TowerData) {
        console.log(isActive, chainId, account, provider);
        console.log(data);
    }

    return (
        <button className={App_module['minting-buttons']} onClick={() => joinQueue(data)}>
            <Icon icon="archive" size={18} />
        </button>
    );
}

// const tower11 = [1, 1, 0, 2, 11, 5];

const tower11 = {
    tier: 1,
    priority: 1,
    operator: 2,
    data1: 2,
    data2: 11,
    data3: 5,
};

export default function App() {
    return (
        <Web3ReactProvider connectors={connectors}>
            <span className={App_module.app}>
                <NavBar />
                <div className={App_module['card-row']}>
                    <TowerCard
                        tower={tower11}
                        // priority={tower11['priority']}
                        // operator={tower11['operator']}
                        // data1={tower11[3]}
                        // data2={tower11[4]}
                        // data3={tower11[5]}
                    />
                    <TowerCard tower={tower11} />
                </div>
                <div className={App_module['card-row']}>
                    <TowerCard tower={tower11} />
                    <TowerCard tower={tower11} />
                    <TowerCard tower={tower11} />
                </div>
                <div className={App_module['card-row']}>
                    <TowerCard tower={tower11} />
                    <TowerCard tower={tower11} />
                </div>
                <div className={App_module['minting-bar']}>
                    <button className={App_module['minting-buttons']}>
                        <Icon icon="refresh" size={18} />
                    </button>
                    <Submit {...tower11} />
                </div>
            </span>
        </Web3ReactProvider>
    );
}
