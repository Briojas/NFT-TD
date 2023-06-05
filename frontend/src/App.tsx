import { useWeb3React, Web3ReactHooks, Web3ReactProvider } from '@web3-react/core';
import type { MetaMask } from '@web3-react/metamask';

import { hooks as metaMaskHooks, metaMask } from './connectors/metamask';
import { getName } from './utils';
import { NavBar } from './components/nav-bar/nav-bar';
import { TowerCard } from './components/tower-card/tower-card';
import App_module from './App.module.scss';

const connectors: [MetaMask, Web3ReactHooks][] = [[metaMask, metaMaskHooks]];

function Child() {
    const { connector } = useWeb3React();
    console.log(`Priority Connector is: ${getName(connector)}`);
    return null;
}

export default function App() {
    return (
        <Web3ReactProvider connectors={connectors}>
            <Child />
            <span className={App_module.app}>
                <NavBar />
                <div className={App_module['card-row']}>
                    <TowerCard
                        tier={1}
                        operator={'plus'}
                        priority={1}
                        data1={3}
                        data2={10}
                        data3={1}
                        className={App_module.cards}
                    />
                    <TowerCard
                        tier={1}
                        operator={'minus'}
                        priority={2}
                        data1={5}
                        data2={8}
                        data3={3}
                    />
                </div>
                <div className={App_module['card-row']}>
                    <TowerCard
                        tier={2}
                        operator={'cross'}
                        priority={3}
                        data1={7}
                        data2={2}
                        data3={9}
                        className={App_module.cards}
                    />
                    <TowerCard
                        tier={2}
                        operator={'code'}
                        priority={4}
                        data1={'Greater than'}
                        data2={0}
                        data3={1}
                    />
                    <TowerCard
                        tier={2}
                        operator={'divide'}
                        priority={5}
                        data1={2}
                        data2={4}
                        data3={7}
                    />
                </div>
                <div className={App_module['card-row']}>
                    <TowerCard
                        tier={3}
                        operator={'code'}
                        priority={6}
                        data1={'Less than'}
                        data2={0}
                        data3={1}
                        className={App_module.cards}
                    />
                    <TowerCard
                        tier={3}
                        operator={'code'}
                        priority={7}
                        data1={'Divisible by'}
                        data2={7}
                        data3={1}
                    />
                </div>
            </span>
        </Web3ReactProvider>
    );
}
