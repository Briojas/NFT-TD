import Metamask from './components/web-3-button/metamask';
import Wrapper from './components/web-3-button/wrapper';

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
