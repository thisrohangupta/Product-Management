import { getAllYamlFiles } from '../lib/getYamls';
import YamlCard from './YamlCard';

export default function Gallery() {
  const yamls = getAllYamlFiles();

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      {yamls.map((y, idx) => (
        <YamlCard key={idx} file={y} />
      ))}
    </div>
  );
}
