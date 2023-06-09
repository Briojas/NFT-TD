import { useWeb3React, Web3ReactHooks, Web3ReactProvider } from '@web3-react/core';
import type { MetaMask } from '@web3-react/metamask';

import { hooks as metaMaskHooks, metaMask } from './connectors/metamask';
import { getName } from './utils';
import { NavBar } from './components/nav-bar/nav-bar';
import { TowerCard, TowerData } from './components/tower-card/tower-card';
import { Icon } from '@blueprintjs/core';
import App_module from './App.module.scss';
import { useEffect, useState } from 'react';
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

export default function App() {
    const [tower11, setTower11] = useState({
        tier: 3,
        priority: 1,
        operator: 0,
        data1: 2,
        data2: 11,
        data3: 5,
    });

    return (
        <Web3ReactProvider connectors={connectors}>
            <span className={App_module.app}>
                <NavBar />
                <div className={App_module['card-row']}>
                    <TowerCard tower={tower11} update={setTower11} />
                    {/* <TowerCard tower={tower11} update={setTower11} /> */}
                </div>
                <div className={App_module['card-row']}>
                    {/* <TowerCard tower={tower11} update={setTower11} />
                    <TowerCard tower={tower11} update={setTower11} />
                    <TowerCard tower={tower11} update={setTower11} /> */}
                </div>
                <div className={App_module['card-row']}>
                    {/* <TowerCard tower={tower11} update={setTower11} />
                    <TowerCard tower={tower11} update={setTower11} /> */}
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
