import Metamask from './components/connect/metamask';
import Wrapper from './components/connect/wrapper';

export default function App() {
    return (
        <>
            <Wrapper />
            <div style={{ display: 'flex', flexFlow: 'wrap', fontFamily: 'sans-serif' }}>
                <Metamask />
            </div>
        </>
    );
}
