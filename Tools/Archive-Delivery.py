"""Archive the playable Windows folder, omitting debug symbols and local save data."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from shutil import copyfile

root=Path(__file__).resolve().parent.parent
delivery=root/'Deliverables'
windows=delivery/'Windows'
assert (windows/'Terreno.exe').is_file(), 'Build the Windows package first.'
copyfile(root/'Tools'/'Delivery-README.txt',delivery/'LEEME.txt')
copyfile(root/'docs'/'CREDITOS_MODELOS.md',delivery/'CREDITOS_MODELOS.md')
target=delivery/'TimeOut_Avance_18Nov2026.zip'
temporary=target.with_suffix('.zip.part')
with ZipFile(temporary,'w',compression=ZIP_DEFLATED,compresslevel=1,allowZip64=True) as archive:
    for path in sorted(windows.rglob('*')):
        if not path.is_file() or path.suffix.lower()=='.pdb' or 'Saved' in path.relative_to(windows).parts:
            continue
        if path.name=='Manifest_DebugFiles_Win64.txt':continue
        archive.write(path,path.relative_to(delivery))
    archive.write(delivery/'LEEME.txt','LEEME.txt')
    archive.write(delivery/'CREDITOS_MODELOS.md','CREDITOS_MODELOS.md')
    archive.write(root/'README.md','README.md')
    for path in sorted((root/'docs').rglob('*')):
        if path.is_file():archive.write(path,path.relative_to(root))
temporary.replace(target)
with ZipFile(target) as archive:
    assert archive.testzip() is None, 'ZIP integrity check failed.'
    assert 'Windows/Terreno.exe' in archive.namelist()
    assert 'CREDITOS_MODELOS.md' in archive.namelist()
    assert 'docs/CATALOGO_BLUEPRINTS.md' in archive.namelist()
    assert not any(n.startswith(('Promocional/','docs/academica/')) for n in archive.namelist())
    assert 'Windows/Terreno/Content/Paks/Terreno-Windows.utoc' in archive.namelist()
print(str(target))
print('ZIP_BYTES',target.stat().st_size)
