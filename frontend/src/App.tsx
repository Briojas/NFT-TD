import styles from './App.module.scss';

import MetaMaskCard from './components/ConnectorCards/MetamaskCard';
// import NetworkCard from './components/ConnectorCards/NetworkCard';
// import WalletConnectCard from './components/ConnectorCards/WalletConnectCard';
import ProviderExample from './components/example';

export default function App() {
    return (
        <>
            <ProviderExample />
            <div style={{ display: 'flex', flexFlow: 'wrap', fontFamily: 'sans-serif' }}>
                <MetaMaskCard />
                {/* <WalletConnectCard />
                <NetworkCard /> */}
            </div>
        </>
    );
}
